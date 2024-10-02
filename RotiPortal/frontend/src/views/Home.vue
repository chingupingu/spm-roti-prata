<template>
    <div class="container">
        <div class="row fixed-top pt-4 bg-white">
            <h1 class="mb-4 display-3">RotiPortal</h1>
            <!-- Logout Button -->
            <div class="col d-flex justify-content-end pe-5 pt-4 position-absolute">
                <button class="btn btn-danger" @click="logout">
                    Logout
                </button>
            </div>
            <!-- Navigation Tabs -->
            <ul class="nav nav-tabs justify-content-center mb-4">
                <!-- WFH dashboard -->
                <li class="nav-item">
                    <a class="nav-link" :class="{ active: activeTab === 'staff' }" href="#"
                        @click.prevent="activeTab = 'staff'">WFH Dashboard</a>
                </li>
                <!-- schedule -->
                <li class="nav-item" v-if="role == 3">
                    <a class="nav-link" :class="{ active: activeTab === 'schedule' }" href="#"
                        @click.prevent="activeTab = 'schedule'">Own Schedule</a>
                </li>
                <!-- manager approval -->
                <li class="nav-item" v-if="role == 3">
                    <a class="nav-link" :class="{ active: activeTab === 'manager' }" href="#"
                        @click.prevent="activeTab = 'manager'">Manager Approval</a>
                </li>
                <!-- company schedule -->
                <li class="nav-item" v-if="role == 1">
                    <a class="nav-link" :class="{ active: activeTab === 'companySchedule' }" href="#"
                        @click.prevent="activeTab = 'companySchedule'">Company Schedule</a>
                </li>
                <!-- management report -->
                <li class="nav-item" v-if="role == 1">
                    <a class="nav-link" :class="{ active: activeTab === 'report' }" href="#"
                        @click.prevent="activeTab = 'report'">Management Report</a>
                </li>
                <!-- TESTING  -->
                <li class="nav-item" v-if="role == 1">
                    <a class="nav-link" :class="{ active: activeTab === 'testing' }" href="#"
                        @click.prevent="activeTab = 'testing'">TESTING</a>
                </li>
            </ul>
        </div>


        <!-- Staff Dashboard -->
        <div v-if="activeTab === 'staff'">
            <div class="row align-items-start" style="margin-top: 150px;">
                <h2>WFH Dashboard</h2>
                <div class="col-12">
                    <div class="card mb-4 p-3">
                        <div class="card-body">
                            <h5 class="card-title mb-4">Apply for Work From Home</h5>
                            <form @submit.prevent="submitWfhRequest">
                                <!-- <div class="mb-3">
                                    <label for="wfhDate" class="form-label">Date</label>
                                    <input type="date" id="wfhDate" v-model="wfhRequest.date" class="form-control"
                                        required>
                                </div> -->
                                <div class="row">
                                    <div class="col mb-3">
                                        <label for="wfhDate" class="form-label">Date</label>
                                        <v-date-picker v-model="wfhRequest.date" class="form-control">
                                        <template v-slot="{ inputValue, inputEvents }">
                                            <input
                                            id="wfhDate"
                                            :value="inputValue"
                                            v-on="inputEvents"
                                            class="form-control"
                                            required
                                            />
                                        </template>
                                        </v-date-picker>
                                    </div>
                                    <div class="col mb-3">
                                        <label for="shift" class="form-label">Shift</label>
                                        <select name="shift" id="shift" v-model="wfhRequest.shift" class="form-select">
                                            <option value="AM">AM</option>
                                            <option value="PM">PM</option>
                                            <option value="FD">Full Day</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col mb-3">
                                    <label for="recurring" class="form-label">Arrangement</label>
                                    <select name="recurring" id="recurring" v-model="wfhRequest.recurring" class="form-select">
                                        <option value="true">Recurring</option>
                                        <option value="false">Non-Recurring</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label for="reason" class="form-label">Reason</label>
                                    <textarea id="reason" v-model="wfhRequest.reason" class="form-control" rows="3" required></textarea>
                                </div>
                                <div class="mb-3">
                                    <label for="attachments" class="form-label">Attachments</label>
                                    <input type="file" id="attachments" v-on:change="wfhRequest.attachments" class="form-control">
                                </div>
                                <button type="submit" class="btn btn-primary">Submit Request</button>
                            </form>
                        </div>
                    </div>
                </div>
                <div class="col-12">
                    <div class="card mb-4">
                        <div class="card-body">
                            <h5 class="card-title">Your WFH Requests</h5>
                            <ul class="list-group">
                                <li v-for="request in wfhRequests" :key="request.id"
                                    class="list-group-item d-flex justify-content-between align-items-center">
                                    {{ request.type }} - {{ request.date }}
                                    <span
                                        :class="['badge', request.status === 'Approved' ? 'bg-success' : 'bg-warning']">{{
                                        request.status }}</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Manager View Schedule Dashboard -->
        <div v-if="activeTab === 'schedule'">
            <div class="row align-items-start" style="margin-top: 200px;">
                <h2>Own Schedule</h2>
                <ScheduleView />
            </div>
        </div>

        <!-- Manager Approval Dashboard -->
        <div v-if="activeTab === 'manager'">
            <div class="row align-items-start" style="margin-top: 200px;">
                <h2>Manager Approval Dashboard</h2>

                <!-- Filter Section -->
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="statusFilter" class="form-label">Filter by Status:</label>
                        <select id="statusFilter" v-model="statusFilter" class="form-select">
                            <option value="">All</option>
                            <option value="Pending">Pending</option>
                            <option value="Approved">Approved</option>
                            <option value="Rejected">Rejected</option>
                        </select>
                    </div>

                    <div class="col-md-4">
                        <label for="teamMemberFilter" class="form-label">Filter by Team Member:</label>
                        <input id="teamMemberFilter" v-model="teamMemberFilter" class="form-control" placeholder="Enter team member name">
                    </div>

                    <!-- <div class="col-md-4">
                        <label for="dateFilter" class="form-label">Filter by Date Range:</label>
                        <input type="date" v-model="startDate" class="form-control mb-1" placeholder="Start Date">
                        <input type="date" v-model="endDate" class="form-control" placeholder="End Date">
                    </div> -->
                </div>

                <div class="row mb-3">
                    <div class="col-md-12">
                        <button @click="filterRequests" class="btn btn-primary">Apply Filters</button>
                    </div>
                </div>

                <!-- Requests Table -->
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Requests</h5>
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
                                    v-for="request in filteredRequests" 
                                    :key="request.id" 
                                    :class="{'table-warning': request.status === 'Pending', 'table-success': request.status === 'Approved'}"
                                >
                                    <td>{{ request.staff_id }}</td>
                                    <td>{{ request.date }}</td>
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

                <!-- Comment Modal -->
                <!-- <div v-if="showCommentModal" class="modal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Reason for {{ actionType === 'approve' ? 'Approval' : 'Rejection' }}</h5>
                                <button type="button" class="btn-close" @click="closeCommentModal"></button>
                            </div>
                            <div class="modal-body">
                                <textarea v-model="comment" class="form-control" placeholder="Enter your reason"></textarea>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="closeCommentModal">Cancel</button>
                                <button type="button" class="btn btn-primary" @click="submitApprovalOrRejection">Submit</button>
                            </div>
                        </div>
                    </div>
                </div> -->

                <!-- Confirmation Modal -->
                <!-- <div v-if="showConfirmationModal" class="modal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Confirmation</h5>
                                <button type="button" class="btn-close" @click="closeConfirmationModal"></button>
                            </div>
                            <div class="modal-body">
                                <p>{{ confirmationMessage }}</p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-primary" @click="closeConfirmationModal">OK</button>
                            </div>
                        </div>
                    </div>
                </div> -->
            </div>
        </div>

        <!-- TESTING -->
        <div v-if="activeTab === 'testing'">
            <div class="row align-items-start" style="margin-top: -130px;">
                <h2>TESTING</h2>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Pending Requests</h5>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Employee</th>
                                    <th>Type</th>
                                    <th>Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(employee, index) in employees" :key="employee.Staff_ID">
                                    <td>{{ employee.Email }}</td>
                                    <td>{{ employee.Country }}</td>
                                    <td>{{ employee.Position }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Management Report -->
        <div v-if="activeTab === 'report'">
            <div class="row align-items-start" style="margin-top: 150px;">
                <h2>Management Report</h2>
                <div class="row">
                    <div class="col-md-6">
                        <div class="card mb-4">
                            <div class="card-body">
                                <h5 class="card-title">Today's Office Presence</h5>
                                <div class="display-4">75%</div>
                                <p class="text-muted">45 out of 60 employees in office</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card mb-4">
                            <div class="card-body">
                                <h5 class="card-title">Weekly WFH Trend</h5>
                                <div class="placeholder-glow">
                                    <span class="placeholder col-12" style="height: 200px;"></span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Department Breakdown</h5>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Department</th>
                                    <th>Total Staff</th>
                                    <th>In Office</th>
                                    <th>WFH</th>
                                    <th>WFH %</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="dept in departmentBreakdown" :key="dept.name">
                                    <td>{{ dept.name }}</td>
                                    <td>{{ dept.totalStaff }}</td>
                                    <td>{{ dept.inOffice }}</td>
                                    <td>{{ dept.wfh }}</td>
                                    <td>{{ dept.wfhPercentage }}%</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
// import { collection, doc, getDocs, deleteDoc } from "firebase/firestore"
// import { deleteObject, ref, getDownloadURL } from "firebase/storage"
// import { firebase_firestore, firebase_storage } from "../firebase"
import { DatePicker } from 'v-calendar';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import ScheduleView from '../components/ScheduleView.vue';

export default {
    components: {
        VDatePicker: DatePicker,
        ScheduleView
    },
    // setup() {
    //     const toast = useToast()
    // },
    data() {
        return {
            employees: [],
            isLoading: true,
            employee_obj: {},
            role: 0,
            activeTab: 'staff',
            wfhRequest: {
                staff_id: '',
                date: '',
                shift: 'FD',
                reason: '',
                recurring: false,
                attachments: null,
                status: 'Pending'
            },
            wfhRequests: [
                { id: 1, type: 'Regular', date: '2023-06-16', status: 'Approved' },
                { id: 2, type: 'Ad-hoc', date: '2023-06-20', status: 'Pending' }
            ],
            pendingRequests: [
                { id: 1, employee: 'John Doe', type: 'Regular', date: '2023-06-16' },
                { id: 2, employee: 'Jane Smith', type: 'Ad-hoc', date: '2023-06-20' }
            ],
            departmentBreakdown: [
                { name: 'Engineering', totalStaff: 20, inOffice: 15, wfh: 5, wfhPercentage: 25 },
                { name: 'Marketing', totalStaff: 15, inOffice: 10, wfh: 5, wfhPercentage: 33 },
                { name: 'Sales', totalStaff: 25, inOffice: 20, wfh: 5, wfhPercentage: 20 }
            ],
            statusFilter: '',         // Initialize the status filter
            teamMemberFilter: '',     // Initialize the team member filter
            startDate: null,         // Initialize start date
            endDate: null,           // Initialize end date
            pendingRequests: [],      // This will hold all pending requests
            filteredRequests: []     // This will hold filtered requests

        }
    },
    methods: {
        submitWfhRequest() {
            // Logic to submit WFH request
            // console.log('Submitting WFH request:', this.wfhRequest)
            axios.post("http://localhost:5000/wfh_request", this.wfhRequest)
            const toast = useToast()
            .then(response => {
                console.log(response.data)
                if (response.status == 201) {
                    toast.success('Request submitted successfully!', {
                        position: 'top-right',
                        timeout: 5000,
                        closeOnClick: true,
                        pauseOnFocusLoss: true,
                        pauseOnHover: true,
                        draggable: true,
                        draggablePercent: 0.6,
                        showCloseButtonOnHover: false,
                        hideProgressBar: true,
                        closeButton: 'button',
                        icon: true,
                        rtl: false
                    })
                } else {
                    toast.error('Request submission failed', {
                        position: 'top-right',
                        timeout: 5000,
                        closeOnClick: true,
                        pauseOnFocusLoss: true,
                        pauseOnHover: true,
                    })
                    throw new Error('Request submission failed')
                }
            })
            .catch(error => {
                console.log(error)
                toast.error('Request could not be submitted. Please try again.', {
                        position: 'top-right',
                        timeout: 5000,
                        closeOnClick: true,
                        pauseOnFocusLoss: true,
                        pauseOnHover: true,
                    })
            })
            // Reset form after submission
            this.wfhRequest = {date: '', reason: '', attachments: null}
        },
        approveRequest(id) {
            // Logic to approve request
            console.log('Approving request:', id)
        },
        rejectRequest(id) {
            // Logic to reject request
            console.log('Rejecting request:', id)
        },
        logout() {
            this.$router.push({ path: `/`, replace: true })
            sessionStorage.clear()
        },
        async fetchEmployeeData() {
            // const employeeCollection = collection(firebase_firestore, "Employee")

            try {
                const fetchedEmployees = await axios.get("http://localhost:5000/employee")
                // const querySnapshot = await getDocs(employeeCollection)
                // let fetchedEmployees = []

                // for (const doc of querySnapshot.docs) {
                // // Access the data from each document
                // const employeeData = doc.data()

                // // Append the employee data to the fetchedEvents array
                // fetchedEmployees.push({ ...employeeData, id: doc.id })
                // console.log(employeeData)
                // }

                // Set the fetchedEmployees data in your component's data
                this.employees = fetchedEmployees
                this.isLoading = false
                // console.log(fetchedEmployees)
            } catch (error) {
                console.error("Error getting documents: ", error)
            }
        },
        async fetchWorkArrangements() { 
            const workArrangementsRef = collection(firebase_firestore, 'WfhRequest'); // Change the collection name to 'WfhRequest'
            
            try {
                const querySnapshot = await getDocs(workArrangementsRef);
                let fetchedRequests = []; // Initialize an array to hold the fetched requests

                for (const doc of querySnapshot.docs) {
                    // Access the data from each document
                    const requestData = doc.data();

                    // Append the request data to the fetchedRequests array
                    fetchedRequests.push({ ...requestData, id: doc.id });
                    console.log(requestData); // Log each fetched request
                }

                // Set the fetchedRequests data in your component's data
                this.requests = fetchedRequests; 
                this.filteredRequests = this.requests; // Initialize filtered requests
                console.log("Fetched Requests:", this.requests); // Log all fetched requests
            } catch (error) {
                console.error("Error getting documents: ", error);
            }
        },
        filterRequests() {
            // Reset filteredRequests to the full list of requests
            this.filteredRequests = this.requests;

            // Filter by Status
            if (this.statusFilter) {
                this.filteredRequests = this.filteredRequests.filter(request => request.status === this.statusFilter);
            }
            console.log("statusFilter:", this.statusFilter);

            // Filter by Team Member (staff_id)
            if (this.teamMemberFilter) {
                this.filteredRequests = this.filteredRequests.filter(request => 
                    request.staff_id.toLowerCase().includes(this.teamMemberFilter.toLowerCase())
                );
            }

            // Filter by Date Range
            if (this.startDate || this.endDate) {
                this.filteredRequests = this.filteredRequests.filter(request => {
                    const requestDate = new Date(request.date);
                    const start = this.startDate ? new Date(this.startDate) : null;
                    const end = this.endDate ? new Date(this.endDate) : null;

                    // Check if the request date is within the specified range
                    return (!start || requestDate >= start) && (!end || requestDate <= end);
                });
            }

            console.log("Filtered Requests:", this.filteredRequests);
        }
    },
    mounted() {
        this.employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
        this.role = this.employee_obj.Role
        this.wfhRequest.staff_id = this.employee_obj.Staff_ID
        // setTimeout(() => {
        // // Once data is loaded, set isLoading to false
        // this.fetchEmployeeData() // Fetch employee when the component is mounted
        // }, 500)
    }
}
</script>

<style scoped>
/* Add any component-specific styles here */
.table-warning {
    background-color: #fff3cd; /* Light yellow for pending requests */
}
.table-success {
    background-color: #d4edda; /* Light green for approved requests */
}
</style>