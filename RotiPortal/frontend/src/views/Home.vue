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
        <div v-if="activeTab === 'staff'" class="staff-dashboard">
            <div class="row align-items-start" style="margin-top: 120px;">
                <h2 class="mb-4">WFH Dashboard</h2>
                <div class="col-12">
                    <div class="card mb-4 p-3">
                        <div class="card-body">
                            <h5 class="card-title mb-4">Apply for Work From Home</h5>
                            <form @submit.prevent="validateWfhRequest">
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
                                        <span class="text-danger">{{ wfh_request_error }}</span>
                                    </div>
                                    <div class="col mb-3">
                                        <label for="shift" class="form-label">Shift</label>
                                        <select name="shift" id="shift" v-model="wfhRequest.shift" class="form-select">
                                            <option value="FD">Full Day</option>
                                            <option value="AM">AM</option>
                                            <option value="PM">PM</option>
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
                            <div class="table-responsive">
                                <div class="row mt-4">
                                    <span v-if="sortedYourRequests.length == 0" class="text-muted fw-light"> No requests to display. </span>
                                    <ul class="list-group">
                                        <li v-for="request in sortedYourRequests" :key="request.request_id"
                                            class="list-group-item d-flex justify-content-between align-items-center">
                                            {{ formatDateToDD_MMM_YYYY(request.date) }} - {{ request.shift === 'FD' ? 'Full Day' : request.shift }}
                                            <div class="col">
                                                
                                            </div>
                                            <span
                                                :class="['badge', request.status === 'Approved' ? 'bg-success' : 'bg-warning']">{{
                                                request.status }}</span>
                                            <button class="btn btn-primary ms-4" data-bs-toggle="modal" data-bs-target="#requestModal" @click="viewRequest(request.request_id)">View</button>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- individual request modal -->
                <div id="requestModal" class="modal" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">WFH Request Details</h5>
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
                                            <th>Recurring:</th>
                                            <td>{{ selectedRequest.recurring }}</td>
                                        </tr>
                                        <tr>
                                            <th>Reason:</th>
                                            <td>{{ selectedRequest.reason }}</td>
                                        </tr>
                                        <tr>
                                            <th>Attachments:</th>
                                            <td>{{ selectedRequest.attachments }}</td>
                                        </tr>
                                        <tr>
                                            <th>Status:</th>
                                            <td>{{ selectedRequest.status }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Manager View Schedule Dashboard -->
        <div v-if="activeTab === 'schedule'" class="own-schedule">
            <div class="row align-items-start" style="margin-top: 120px;">
                <h2>Own Schedule</h2>
                <ScheduleView />
            </div>
        </div>

        <!-- Manager Approval Dashboard -->
        <div v-if="activeTab === 'manager'" class="manager-dashboard">
            <div class="row align-items-start" style="margin-top: 120px;">
                <h2 class="mb-4">Manager Approval Dashboard</h2>

                <!-- Filter Section -->
                <div class="row mb-4">
                    <div class="col-md-6 d-flex flex-column">
                        <label for="statusFilter" class="form-label">Filter by Status:</label>
                        <select id="statusFilter" v-model="statusFilter" class="form-select">
                            <option value="">All</option>
                            <option value="Pending">Pending</option>
                            <option value="Approved">Approved</option>
                            <option value="Rejected">Rejected</option>
                        </select>
                    </div>

                    <div class="col-md-6 d-flex flex-column">
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
                                        :class="{'table-warning': request.status === 'Pending', 'table-success': request.status === 'Approved', 'table-danger': request.status === 'Rejected'}"
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
                                            >
                                                Approve
                                            </button>
                                            <button 
                                                @click="openCommentModal('reject', request.request_id)" 
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

                        <!-- Comment Modal -->
                        <div v-if="commentModalVisible" class="custom-backdrop fade show"></div>
                        <div v-if="commentModalVisible" class="modal fade show" style="display: block;" tabindex="-1">
                            <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title">{{ actionType === 'approve' ? 'Approve Request' : 'Reject Request' }}</h5>
                                        <button type="button" class="btn-close" @click="commentModalVisible = false"></button>
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
                                        <button type="button" class="btn btn-secondary" @click="commentModalVisible = false">Cancel</button>
                                        <button type="button" class="btn btn-primary" @click="submitComment">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>

        <!-- TESTING -->
        <div v-if="activeTab === 'testing'" class="testing-dashboard">
            <div class="row align-items-start" style="margin-top: 155px;">
                <h2 class="mb-4">TESTING</h2>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Pending Requests</h5>
                        <div class="table-responsive">
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
        </div>

        <!-- Management Report -->
        <div v-if="activeTab === 'report'" class="management-report">
            <div class="row align-items-start" style="margin-top: 155px;">
                <h2 class="mb-4">Management Report</h2>
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
                        <div class="table-responsive">
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

    </div>
</template>

<script>
// import { collection, doc, getDocs, deleteDoc } from "firebase/firestore"
// import { deleteObject, ref, getDownloadURL } from "firebase/storage"
// import { firebase_firestore, firebase_storage } from "../firebase"
import { DatePicker } from 'v-calendar';
import axios from 'axios';
import ScheduleView from '../components/ScheduleView.vue';

export default {
    components: {
        VDatePicker: DatePicker,
        ScheduleView
    },
    data() {
        return {
            // general data
            employee_obj: {},
            role: 0,
            activeTab: 'staff',

            // wfh request data
            wfhRequest: {
                staff_id: '',
                date: '',
                shift: 'FD',
                reason: '',
                recurring: false,
                attachments: null,
                status: 'Pending'
            },
            your_requests: [],
            wfh_request_error: '',
            selectedRequest: {},

            // manager approval data
            employees: [],
            isLoading: true,
            statusFilter: '',         // Initialize the status filter
            teamMemberFilter: '',     // Initialize the team member filter
            dateMatch: null,         // Initialize the date filter
            employee_requests: [],      // This will hold all employee requests

            commentModalVisible: false, // Control visibility of the modal
            actionType: '',             // To store whether it's 'approve' or 'reject'
            requestId: null,            // Store the request ID for the selected action
            comment: '',                // Store the comment input from the user
            
            departmentBreakdown: [
                { name: 'Engineering', totalStaff: 20, inOffice: 15, wfh: 5, wfhPercentage: 25 },
                { name: 'Marketing', totalStaff: 15, inOffice: 10, wfh: 5, wfhPercentage: 33 },
                { name: 'Sales', totalStaff: 25, inOffice: 20, wfh: 5, wfhPercentage: 20 }
            ]

        }
    },
    computed: {
        sortedYourRequests() {
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Set to start of day for accurate comparison
        return [...this.your_requests]
            .filter(request => new Date(request.date) >= today)
            .sort((a, b) => new Date(a.date) - new Date(b.date));
    },
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
        return [...filtered].sort((a, b) => new Date(a.date) - new Date(b.date));
    },
    },
    methods: {
        getStaffName(staff_id) {
            for (const employee of this.employees) {
                if (employee.Staff_ID == staff_id) {
                    return employee.Staff_FName + " " + employee.Staff_LName
                }
            }
        },
        validateWfhRequest() {
            // Logic to validate WFH request
            axios.post("http://localhost:5000/wfh_request/validate", this.wfhRequest)
            .then(response => {
                if (response.data.valid) {
                    this.submitWfhRequest()
                } else {
                    window.alert(response.data.message)
                    this.wfh_request_error = response.data.message
                }
            })
            .catch(error => {
                console.log(error)
            })
        },
        submitWfhRequest() {
            // Logic to submit WFH request
            axios.post("http://localhost:5000/wfh_request", this.wfhRequest)
            .then(response => {
                console.log(response.data)
                if (response.status == 201) {
                    window.alert('Request submitted successfully!')
                    // Reset form after submission
                    this.wfhRequest = {
                        staff_id: this.employee_obj.Staff_ID,
                        date: '',
                        shift: 'FD',
                        reason: '',
                        recurring: false,
                        attachments: null,
                        status: 'Pending'
                    }
                    this.populateWfhRequests()
                }
                // } else {
                //     window.alert(response.data.error)
                //     throw new Error('Request submission failed')
                // }
            })
            .catch(error => {
                // console.log(error)
                // window.alert('Request could not be submitted. Please try again.')
                window.alert(error.response.data.error)
            })
        },
        populateWfhRequests() {
            axios.get(`http://localhost:5000/wfh_request/staff/${this.employee_obj.Staff_ID}`)
            .then(response => {
                this.your_requests = response.data
            })
            .catch(error => {
                this.your_requests_error = error.response.data.error
            })
        },
        viewRequest(request_id) {
            axios.get(`http://localhost:5000/wfh_request/${request_id}`)
            .then(response => {
                this.selectedRequest = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },
        // approveRequest(id) {
        //     // Logic to approve request
        //     console.log('Approving request:', id)
        // },
        // rejectRequest(id) {
        //     // Logic to reject request
        //     console.log('Rejecting request:', id)
        // },
        logout() {
            this.$router.push({ path: `/`, replace: true })
            sessionStorage.clear()
        },
        openCommentModal(actionType, requestId) {
            console.log(requestId)
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

                // Submit the comment and status update
                if (this.actionType === 'approve') {
                    this.approveRequest(this.requestId, this.comment);
                } else if (this.actionType === 'reject') {
                    this.rejectRequest(this.requestId, this.comment);
                }
            }

            // Hide the modal after submission
            this.commentModalVisible = false;
        },
        approveRequest(requestId, comment) {
            const payload = {
                status: 'Approved',
                comment: comment
            };

            // Make the API call to update the status in the backend
            axios.put(`http://localhost:5000/wfh_request/${requestId}`, payload)
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
        rejectRequest(requestId, comment) {
            const payload = {
                status: 'Rejected', // Change the status to Rejected
                comment: comment    // Add the comment
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
            axios.put(`http://localhost:5000/wfh_request/${requestId}`, payload)
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
        // async fetchWorkArrangements() { 
        //     const workArrangementsRef = collection(firebase_firestore, 'WfhRequest'); // Change the collection name to 'WfhRequest'
            
        //     try {
        //         const querySnapshot = await getDocs(workArrangementsRef);
        //         let fetchedRequests = []; // Initialize an array to hold the fetched requests

        //         for (const doc of querySnapshot.docs) {
        //             // Access the data from each document
        //             const requestData = doc.data();

        //             // Append the request data to the fetchedRequests array
        //             fetchedRequests.push({ ...requestData, id: doc.id });
        //             console.log(requestData); // Log each fetched request
        //         }

        //         // Set the fetchedRequests data in your component's data
        //         this.requests = fetchedRequests; 
        //         this.filteredRequests = this.requests; // Initialize filtered requests
        //         console.log("Fetched Requests:", this.requests); // Log all fetched requests
        //     } catch (error) {
        //         console.error("Error getting documents: ", error);
        //     }
        // },
        // filterRequests() {
        //     // Reset filteredRequests to the full list of requests
        //     this.filteredRequests = this.requests;

        //     // Filter by Status
        //     if (this.statusFilter) {
        //         this.filteredRequests = this.filteredRequests.filter(request => request.status === this.statusFilter);
        //     }
        //     console.log("statusFilter:", this.statusFilter);

        //     // Filter by Team Member (staff_id)
        //     if (this.teamMemberFilter) {
        //         this.filteredRequests = this.filteredRequests.filter(request => 
        //             request.staff_id.toLowerCase().includes(this.teamMemberFilter.toLowerCase())
        //         );
        //     }

        //     // Filter by Date Range
        //     if (this.startDate || this.endDate) {
        //         this.filteredRequests = this.filteredRequests.filter(request => {
        //             const requestDate = new Date(request.date);
        //             const start = this.startDate ? new Date(this.startDate) : null;
        //             const end = this.endDate ? new Date(this.endDate) : null;

        //             // Check if the request date is within the specified range
        //             return (!start || requestDate >= start) && (!end || requestDate <= end);
        //         });
        //     }

        //     console.log("Filtered Requests:", this.filteredRequests);
        // },
        formatDateToDD_MMM_YYYY(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
        }
        // formatDateForPicker(date) {
        //     if (!date) return '';
        //     return date.toISOString().split('T')[0];
        // }
    },
    mounted() {
        this.employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
        this.role = this.employee_obj.Role
        this.wfhRequest.staff_id = this.employee_obj.Staff_ID
        this.populateWfhRequests()
        this.fetchEmployeeData()
        
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
.table-danger {
    background-color: #f8d7da; /* Light red for rejected requests */
}

.staff-dashboard,
.manager-dashboard,
.management-report,
.own-schedule,
.testing-dashboard {
    height: calc(100vh - 135px);
    overflow-y: auto;
}

.table-responsive {
    max-height: calc(100vh - 350px);
    overflow-y: auto;
}

/* Adjust card max-height for better visibility */
.card {
    max-height: calc(100vh - 250px);
    overflow-y: auto;
}

.custom-backdrop {
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black */
    position: fixed; /* Position it correctly */
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1040; /* Ensure it's behind the modal */
}
</style>