<template>
    <h2 class="mb-4">Manager Approval Dashboard</h2>
        <!-- Filter Section -->
        <div class="row mb-4">
            <div class="col-md-6">
                <label for="statusFilter" class="form-label">Filter by Status:</label>
                <select id="statusFilter" v-model="statusFilter" class="form-select">
                    <option value="">All</option>
                    <option value="Pending">Pending</option>
                    <option value="Approved">Approved</option>
                    <option value="Rejected">Rejected</option>
                </select>
            </div>

            <div class="col-md-6">
                <label for="teamMemberFilter" class="form-label">Filter by Team Member:</label>
                <input id="teamMemberFilter" v-model="teamMemberFilter" class="form-control" placeholder="Enter team member name">
            </div>
        </div>

        <!-- Requests Table -->
        <div class="card">
            <h5 class="card-title">Requests</h5>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Date</th>
                                <th>Reason</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr 
                                v-for="request in filteredEmployeeRequests" 
                                :key="request.id" 
                                :class="{'table-warning': request.status === 'Pending', 'table-success': request.status === 'Approved'}"
                            >
                                <td>{{ getStaffName(request.staff_id) }}</td>
                                <td>{{ formatDateToDD_MMM_YYYY(request.date) }}</td>
                                <td>{{ request.reason }}</td>
                                <td>{{ request.status }}</td>
                                <td>
                                    <button 
                                        @click="openCommentModal('approve', request.id)" 
                                        class="btn btn-sm btn-success me-2" 
                                        v-if="request.status === 'Pending'"
                                    >
                                        Approve
                                    </button>
                                    <button 
                                        @click="openCommentModal('reject', request.id)" 
                                        class="btn btn-sm btn-danger" 
                                        v-if="request.status === 'Pending'"
                                    >
                                        Reject
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'ManagerApprovalView',
    data() {
        return {
            // general data
            employee_obj: {},

            // manager approval data
            employees: [],
            isLoading: true,
            statusFilter: '',         // Initialize the status filter
            teamMemberFilter: '',     // Initialize the team member filter
            startDate: null,         // Initialize start date
            endDate: null,           // Initialize end date
            employee_requests: [],      // This will hold all employee requests
        }
    },
    computed: {
        filteredEmployeeRequests() {
            const today = new Date();
            today.setHours(0, 0, 0, 0); // Set to start of day for accurate comparison
            const filtered = this.employee_requests.filter(request => {
            const statusMatch = !this.statusFilter || request.status === this.statusFilter;
            const teamMemberMatch = !this.teamMemberFilter || 
                this.getStaffName(request.staff_id).toLowerCase().includes(this.teamMemberFilter.toLowerCase());
            const dateMatch = new Date(request.date) >= today;
            return statusMatch && teamMemberMatch && dateMatch;
        });
        // Sort pending requests to the top, then by earliest date
        return filtered.sort((a, b) => {
            if (a.status === 'Pending' && b.status !== 'Pending') return -1;
            if (a.status !== 'Pending' && b.status === 'Pending') return 1;
            return new Date(a.date) - new Date(b.date);
        });
    },
    },
    methods: {
        approveRequest(request_id) {
            // Logic to approve request
            console.log('Approving request:', request_id)
        },
        rejectRequest(request_id) {
            // Logic to reject request
            console.log('Rejecting request:', request_id)
        },
        getStaffName(staff_id) {
            for (const employee of this.employees) {
                if (employee.Staff_ID == staff_id) {
                    return employee.Staff_FName + " " + employee.Staff_LName
                }
            }
        },
        async fetchEmployeeData() {
            axios.get(`http://localhost:5000/employee/manager/${this.employee_obj.Staff_ID}`)
            .then(response => {
                this.employees = response.data
                this.fetchEmployeeRequests()
            })
            .catch(error => {
                console.log(error)
            })
        },
        async fetchEmployeeRequests() {
            for (const employee of this.employees) {
                axios.get(`http://localhost:5000/wfh_request/staff/${employee.Staff_ID}`)
                .then(response => {
                    this.employee_requests.push(...response.data)
                })
                .catch(error => {
                    console.log(error)
                })
            }
            console.log(this.pendingRequests)
        },
        formatDateToDD_MMM_YYYY(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
        }
    },
    mounted() {
        this.employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
        this.fetchEmployeeData()
    }
}

</script>

