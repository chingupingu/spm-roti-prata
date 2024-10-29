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
                            :key="request.request_id" 
                            :class="{
                                'table-warning': request.status === 'Pending', 
                                'table-success': request.status === 'Approved', 
                                'table-danger': request.status === 'Rejected',
                                'table-secondary': request.status === 'Withdrawn'
                            }"
                        >
                            <td>{{ getStaffName(request.staff_id) }}</td>
                            <td>{{ formatDateToDD_MMM_YYYY(request.date) }}</td>
                            <td>{{ request.reason }}</td>
                            <td>{{ request.status }}</td>
                            <td>
                                <button 
                                    @click="openCommentModal('approve', request.request_id)" 
                                    class="btn btn-sm btn-success me-2" 
                                    v-if="request.status === 'Pending'"
                                    data-bs-toggle="modal" data-bs-target="#commentModal"
                                >
                                    Approve
                                </button>
                                <button 
                                    @click="openCommentModal('reject', request.request_id)" 
                                    class="btn btn-sm btn-danger" 
                                    v-if="request.status === 'Pending'"
                                    data-bs-toggle="modal" data-bs-target="#commentModal"
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

    <!-- Comment Modal -->
    <div id="commentModal" class="modal fade" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ actionType === 'approve' ? 'Approve Request' : 'Reject Request' }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <table class="table table-striped">
                        <tbody>
                            <tr>
                                <th>Date:</th>
                                <td>{{ formatDateToDD_MMM_YYYY(selectedRequest.date) }}</td>
                            </tr>
                            <tr>
                                <th>Shift:</th>
                                <td>{{ selectedRequest.shift }}</td>
                            </tr>
                            <tr>
                                <th>Reason:</th>
                                <td>{{ selectedRequest.reason }}</td>
                            </tr>
                            <tr>
                                <th>Attachments:</th>
                                <td>{{ selectedRequest.attachments }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <textarea v-model="comment" class="form-control" placeholder="Enter your comment for the above request..."></textarea>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" @click="submitComment" data-bs-dismiss="modal">Submit</button>
                </div>
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
            commentModalVisible: false, // Control visibility of the modal
            actionType: '',             // To store whether it's 'approve' or 'reject'
            requestId: null,            // Store the request ID for the selected action
            comment: '',                // Store the comment input from the user
            selectedRequest: {},

            // delegate data
            delegateData: {}
        }
    },
    computed: {
        filteredEmployeeRequests() {
            const today = new Date();
            today.setHours(0, 0, 0, 0); // Set to the start of the day for accurate comparison

            const isWithin24Hours = (requestDate) => {
                let approvalDate = new Date(requestDate);
                approvalDate.setDate(approvalDate.getDate() - 1); // 24 hours before the request date
                
                let daysToSubtract = 0;
                // Adjust for weekends (skip Saturday and Sunday)
                if (approvalDate.getDay() === 0) { // Sunday
                    daysToSubtract = 2;
                } else if (approvalDate.getDay() === 6) { // Saturday
                    daysToSubtract = 1;
                }
                approvalDate.setDate(approvalDate.getDate() - daysToSubtract);

                return today > approvalDate; // Can only approve/reject if today is greater than the adjusted approval date
            };

            const filtered = this.employee_requests.filter(request => {
                const statusMatch = !this.statusFilter || request.status === this.statusFilter;
                const teamMemberMatch = !this.teamMemberFilter ||
                    this.getStaffName(request.staff_id).toLowerCase().includes(this.teamMemberFilter.toLowerCase());
                
                const requestDate = new Date(request.date);
                const dateMatch = !isWithin24Hours(requestDate); // Ensure it's not within 24 hours considering the work week

                return statusMatch && teamMemberMatch && dateMatch;
            });

            // Sort requests: Pending at the top, then Approved, then Rejected
            return filtered.sort((a, b) => {
                const statusOrder = { 'Pending': 0, 'Approved': 1, 'Rejected': 2 };
                if (statusOrder[a.status] !== statusOrder[b.status]) {
                    return statusOrder[a.status] - statusOrder[b.status];
                }
                // If status is the same, sort by date (earliest first)
                return new Date(a.date) - new Date(b.date);
            });
        },
    },
    methods: {
        openCommentModal(actionType, requestId) {
            console.log(requestId)
            // console.log(this.getStaffIdFromRequest(requestId))
            // console.log(this.startDate)
            // console.log(this.endDate)
            // console.log(actionType)
            this.actionType = actionType; // Set the action type (approve or reject)
            this.requestId = requestId;   // Set the request ID
            this.comment = '';             // Reset comment input
            this.commentModalVisible = true; // Show the modal
            this.viewRequest(requestId);
        },
        submitComment() {
            // Find the index of the request by requestId
            const index = this.employee_requests.findIndex(request => request.request_id === this.requestId);
            
            if (index !== -1) {
                // Optimistically update the local status
                const newStatus = this.actionType === 'approve' ? 'Approved' : 'Rejected';
                this.employee_requests[index].status = newStatus;  // Update the status directly
                const staffID = this.employee_requests[index].staff_id
                // const startDate = this.startDate
                // const endDate = this.endDate
                const date = this.employee_requests[index].date
                const shift = this.employee_requests[index].shift
                const actionType = this.actionType

                // Submit the comment and status update
                if (this.actionType === 'approve') {
                    this.approveRequest(this.requestId, this.comment, this.employee_obj.Staff_FName + " " + this.employee_obj.Staff_LName);
                    window.alert('Request approved successfully!')
                    // this.alertStaff(staffID, startDate, endDate, shift, actionType)
                    this.alertStaff(staffID, date, shift, actionType)
                    this.$forceUpdate()
                } else if (this.actionType === 'reject') {
                    this.rejectRequest(this.requestId, this.comment, this.employee_obj.Staff_FName + " " + this.employee_obj.Staff_LName);
                    window.alert('Request rejected successfully!')
                    // this.alertStaff(staffID, startDate, endDate, shift, actionType)
                    this.alertStaff(staffID, date, shift, actionType)
                    this.$forceUpdate()
                }
            }

            // Hide the modal after submission
            this.commentModalVisible = false;
        },
        viewRequest(request_id) {
            axios.get(`http://127.0.0.1:5000/wfh_request/${request_id}`)
            .then(response => {
                this.selectedRequest = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },
        approveRequest(requestId, comment, approving_manager) {
            const payload = {
                status: 'Approved',
                comment: comment,
                approving_manager: approving_manager
            };

            // Make the API call to update the status in the backend
            axios.put(`http://127.0.0.1:5000/wfh_request/${requestId}`, payload)
                .then(() => {  
                })
                .catch(error => {
                    console.error('Error updating request:', error);
                    window.alert('Failed to approve request. Please try again.');
                    
                    // Optionally revert the optimistic update in case of an error
                    const index = this.employee_requests.findIndex(request => request.request_id === requestId);
                    if (index !== -1) {
                        this.employee_requests[index].status = 'Pending';  // Revert to pending
                    }
                });
        },
        rejectRequest(requestId, comment, approving_manager) {
            const payload = {
                status: 'Rejected', // Change the status to Rejected
                comment: comment,    // Add the comment
                approving_manager: approving_manager
            };

            // Find the index of the request in your local data
            const index = this.employee_requests.findIndex(request => request.request_id === requestId);

            // Optimistically update the local state
            if (index !== -1) {
                this.employee_requests[index].status = 'Rejected'; // Update the status to Rejected
                // Optional: Remove it from the list if you want to hide it immediately
                // this.employee_requests.splice(index, 1); // Uncomment if you want to remove the item
            }

            // Send a PUT request to the server to update the request
            axios.put(`http://127.0.0.1:5000/wfh_request/${requestId}`, payload)
                .then(() => {
                    console.log(`Request ${requestId} rejected with comment: ${comment}`);
                })
                .catch(error => {
                    console.error('Error updating request:', error);
                    window.alert('Failed to reject request. Please try again.');
                    // If the request fails, revert the optimistic update
                    if (index !== -1) {
                        this.employee_requests[index].status = 'Pending'; // Revert to pending if needed
                    }
                });
        },

        alertStaff(staffID, date, shift, actionType) {
        // alertStaff(staffID, startDate, endDate, actionType) {
            const payload = {
            staffID: staffID,
            // startDate: startDate,  // Start date for the alert
            // endDate: endDate,      // End date for the alert
            date: date,
            shift: shift,
            actionType: actionType  // Action type (approve or reject)
            }

            axios.post("http://127.0.0.1:5000/wfh_request_update_alert", payload)
            .then(response => {
                console.log(response.data)
                if (response.status == 201) {
                    window.alert('Request submitted successfully!')
                }
            })
            .catch(error => {
                window.alert(error.response.data.error)
            })
        },

        getStaffIdFromRequest(requestId) {
            // Find the request object using the requestId
            const request = this.employee_requests.find(req => req.request_id === requestId);

            // Check if the request exists and return the staff ID
            if (request) {
                return request.staff_id; // Adjust this based on the actual field name
            } else {
                console.error('Request not found');
                return null; // Or handle it as needed
            }
        },

        getStaffName(staff_id) {
            for (const employee of this.employees) {
                if (employee.Staff_ID == staff_id) {
                    return employee.Staff_FName + " " + employee.Staff_LName
                }
            }
        },
        // async fetchEmployeeData(staff_id) {
        //     axios.get(`http://127.0.0.1:5000/employee/manager/${staff_id}`)
        //     .then(response => {
        //         this.employees = response.data
        //         this.fetchEmployeeRequests()
        //     })
        //     .catch(error => {
        //         console.log(error)
        //     })
        // },

        // takes in a list of staff_ids
        async fetchEmployeeData(staff_id_list) {
            for (const staff_id of staff_id_list) {
                try {
                    const response = await axios.get(`http://127.0.0.1:5000/employee/manager/${staff_id}`)
                    this.employees.push(...response.data)
                } catch (error) {
                    console.log(error)
                }
            }
            this.fetchEmployeeRequests()
        },
        async fetchEmployeeRequests() {
            for (const employee of this.employees) {
                axios.get(`http://127.0.0.1:5000/wfh_request/staff/${employee.Staff_ID}`)
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
        },
        isDelegate(staff_id) {
            // check if the staff_id exists in the delegate collection
            axios.get(`http://127.0.0.1:5000/delegate/${staff_id}`)
            .then(response => {
                // if it does, fetch the delegate data
                this.delegateData = response.data
                const today = new Date();
                const startDate = new Date(this.delegateData.start_date);
                const endDate = new Date(this.delegateData.end_date);
                
                // check if the delegation is within the date range
                if (today >= startDate && today <= endDate) {
                    console.log("Delegation valid (within date range)");
                    this.fetchEmployeeData([this.delegateData.manager_id, staff_id])
                } else {
                    console.log("Delegation invalid (not within date range)")
                    this.fetchEmployeeData([staff_id])
                }
            })
            // if the staff_id does not exist in the delegate collection, 
            // fetch the employee data of employees under this manager
            .catch(error => {
                console.log("This employee is not a delegate.")
                this.fetchEmployeeData([staff_id])
                
            })
        },
        cleanupExpiredDelegates() {
            axios.delete('http://127.0.0.1:5000/delegate/cleanup')
            .then(response => {
                console.log(response.data.message)
            })
            .catch(error => {
                console.log(error)
            })
        }
    },
    mounted() {
        this.employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
        this.cleanupExpiredDelegates()
        this.isDelegate(this.employee_obj.Staff_ID)
        // this.fetchEmployeeData()
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
.table-danger {
    background-color: #f8d7da; /* Light red for rejected requests */
}
.table-secondary {
    background-color: #e2e3e5; /* Light grey for withdrawn requests */
}
</style>