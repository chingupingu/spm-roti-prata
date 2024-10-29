<template>
    <!-- Staff Dashboard -->
    <h2 class="mb-4">WFH Dashboard</h2>
    <div class="col-12">
        <div class="card mb-4 p-3">
            <div class="card-body">
                <h5 class="card-title mb-4">Apply for Work From Home</h5>
                <form @submit.prevent="validateWfhRequest">
                    <div class="row mb-3">
                        <h6><label class="form-label">Arrangement</label></h6>
                        <div>
                            <label class="switch">
                                <input type="checkbox" v-model="wfhRequest.recurring" />
                                <span class="slider round"></span>
                            </label>
                            <span class="toggle-text">{{ wfhRequest.recurring ? 'Recurring' : 'Non-Recurring' }}</span>
                        </div>
                    </div>

                    <!-- Non-Recurring Form -->
                    <div v-if="!wfhRequest.recurring">
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
                        <div class="mb-3">
                            <label for="reason" class="form-label">Reason</label>
                            <textarea id="reason" v-model="wfhRequest.reason" class="form-control" rows="3" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="attachments" class="form-label">Attachments</label>
                            <input type="file" id="attachments" v-on:change="wfhRequest.attachments" class="form-control">
                        </div>
                    </div>

                    <!-- Recurring Form -->
                    <div v-else>
                        <div class="mb-3">
                            <!-- Choose your Shift -->
                            <div class="col mb-3">
                                <label for="shift" class="form-label">Shift</label>
                                <select name="shift" id="shift" v-model="wfhRequest.shift" class="form-select">
                                    <option value="FD">Full Day</option>
                                    <option value="AM">AM</option>
                                    <option value="PM">PM</option>
                                </select>
                            </div>
                            <div class="date-picker-box" @click="showDatePicker = !showDatePicker" style="border: 1px solid #ced4da; padding: 10px; cursor: pointer;">
                                <span v-if="wfhRequest.dates.length === 0">Click to select dates</span>
                                <span v-else>{{ wfhRequest.dates.length }} date(s) selected</span>
                            </div>
                            <!-- Date Picker -->
                            <v-date-picker
                                v-if="showDatePicker"
                                v-model="newDate"
                                class="form-control mt-2"
                                :input-attr="{ required: true }"
                            />
                            <button v-if="showDatePicker" @click="addDate" class="btn btn-secondary mt-2">Add Date</button>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Selected Dates:</label>
                            <ul class="list-group">
                                <li v-for="(date, index) in wfhRequest.dates" :key="index" class="list-group-item">
                                    {{ formatDateToDD_MMM_YYYY(date) }}
                                </li>
                            </ul>
                        </div>

                        <div class="mb-3">
                            <label for="recurringReason" class="form-label">Reason for Recurring</label>
                            <textarea id="recurringReason" v-model="wfhRequest.recurringReason" class="form-control" rows="3" required></textarea>
                        </div>
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
                                <div class="col-4">
                                    {{ formatDateToDD_MMM_YYYY(request.date) }} - {{ request.shift === 'FD' ? 'Full Day' : request.shift }}
                                </div>
                                <div class="col-4">
                                    <span
                                        :class="['badge', request.status === 'Approved' ? 'bg-success' : request.status === 'Rejected' ? 'bg-danger' : 'bg-warning']">
                                        {{ request.status }}
                                    </span>
                                </div>
                                <div class="col-2">
                                    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#requestModal" @click="viewRequest(request.request_id)">View</button>
                                </div>
                                <div class="col-2">
                                    <button v-if="request.status === 'Approved'" class="btn btn-secondary ms-2" data-bs-toggle="modal" data-bs-target="#withdrawModal" @click="withdrawRequest(request.request_id)">Withdraw</button>
                                </div>
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
                                <td>{{ selectedRequest.shift === 'FD' ? 'Full Day' : selectedRequest.shift }}</td>
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
                            <tr v-if="selectedRequest.status === 'Approved' || selectedRequest.status === 'Rejected'">
                                <th>Comment:</th>
                                <td>{{ selectedRequest.comment }}</td>
                            </tr>
                            <tr v-if="selectedRequest.status === 'Approved'">
                                <th>Approved By:</th>
                                <td>{{ selectedRequest.approving_manager }}</td>
                            </tr>
                            <tr v-if="selectedRequest.status === 'Rejected'">
                                <th>Rejected By:</th>
                                <td>{{ selectedRequest.approving_manager }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Withdrawal Request Modal -->
    <div id="withdrawModal" class="modal fade" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Withdraw Request</h5>
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
                                <th>Status:</th>
                                <td>{{ selectedRequest.status }}</td>
                            </tr>
                            <tr>
                                <th>Attachments:</th>
                                <td>{{ selectedRequest.attachment_url }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <p><strong>Are you sure you want to withdraw this request?</strong></p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" @click="submitWithdrawalRequest" data-bs-dismiss="modal">Withdraw</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { DatePicker } from 'v-calendar';
import Multiselect from 'vue-multiselect';
import axios from 'axios'
export default {
    name: 'WFHRequestView',
    components: {
        VDatePicker: DatePicker,
        Multiselect
    },
    data() {
        return {
            employee_obj: {},
            wfhRequest: {
                staff_id: '',
                date: '',
                startDate: '',
                endDate: '',
                shift: 'FD',
                reason: '',
                recurring: false,
                recurringReason: '',
                attachments: null,
                status: 'Pending',
                dates: [],
                approving_manager: ''
            },
            newDate: '', // New variable to hold the single date from the date picker
            dates: [], // Options for the multiselect
            your_requests: [],
            wfh_request_error: '',
            selectedRequest: {},
            showDatePicker: false
        }
    },

    computed: {
        sortedYourRequests() {
        // const today = new Date();
        // today.setHours(0, 0, 0, 0); // Set to start of day for accurate comparison
        
        // return [...this.your_requests]
        //     .filter(request => new Date(request.date) >= today && request.status !== 'Withdrawn') // Exclude withdrawn requests
        //     .sort((a, b) => new Date(a.date) - new Date(b.date));

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

            const filtered = this.your_requests.filter(request => {
                const requestDate = new Date(request.date);
                const dateMatch = !isWithin24Hours(requestDate); // Ensure it's not within 24 hours considering the work week

                return dateMatch;
            });

            return filtered.sort((a, b) => {
                // sort by date (earliest first)
                return new Date(a.date) - new Date(b.date);
            });
    }
    },
    methods: {
        getStaffName(staff_id) {
            for (const employee of this.employees) {
                if (employee.Staff_ID == staff_id) {
                    return employee.Staff_FName + " " + employee.Staff_LName
                }
            }
        },
        addDate() {
            if (this.newDate && !this.wfhRequest.dates.includes(this.newDate)) {
                this.wfhRequest.dates.push(this.newDate);
                this.dates.push({ date: this.newDate }); // Add to multiselect options
                this.newDate = ''; // Clear the input field
                console.log(this.wfhRequest.dates);
            }
        },
        validateWfhRequest() {
            // Logic to validate WFH request
            axios.post("http://127.0.0.1:5000/wfh_request/validate", this.wfhRequest)
            .then(response => {
                if (response.data.valid) {
                    if (response.data.message) {
                        this.submitWfhRequest(response.data.message)
                    } else {
                        this.submitWfhRequest(null)
                    }
                } else {
                    window.alert(response.data.message)
                    this.wfh_request_error = response.data.message
                }
            })
            .catch(error => {
                console.log(error)
            })
        },
        submitWfhRequest(message) {
            const requestPayload = {
                ...this.wfhRequest,
                dates: this.wfhRequest.dates.map(date => new Date(date).toISOString()), // Convert to ISO format
            };

            // Logic to submit WFH request
            axios.post("http://127.0.0.1:5000/wfh_request", this.wfhRequest)
            .then(response => {
                console.log(response.data)
                if (response.status == 201) {
                    if (message === null) {
                        window.alert('Request submitted successfully!')
                        this.alertSupervisor()
                    } else {
                        window.alert(message)
                    }
                    // Reset form after submission
                    this.wfhRequest = {
                        staff_id: this.employee_obj.Staff_ID,
                        date: '',
                        shift: 'FD',
                        reason: '',
                        recurring: false,
                        attachments: null,
                        status: 'Pending',
                        dates: [] // Reset dates
                    }
                    this.$forceUpdate()
                    this.populateWfhRequests()
                }
            })
            .catch(error => {
                window.alert(error.response.data.error)
            })
        },
        alertSupervisor() {
            axios.post("http://127.0.0.1:5000/wfh_request_alert", this.wfhRequest)
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
        populateWfhRequests() {
            axios.get(`http://127.0.0.1:5000/wfh_request/staff/${this.employee_obj.Staff_ID}`)
            .then(response => {
                this.your_requests = response.data
            })
            .catch(error => {
                this.your_requests_error = error.response.data.error
            })
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
        formatDateToDD_MMM_YYYY(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
        }, 
        // Method to withdraw a request
        withdrawRequest(requestId) {
            this.selectedRequestId = requestId; // Store the request ID for withdrawal
            axios.get(`http://127.0.0.1:5000/wfh_request/${requestId}`)
            .then(response => {
                this.selectedRequest = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },

        // Submit the withdrawal request
        submitWithdrawalRequest() {
            const payload = {
                status: 'Withdrawn', // Change the status to Withdrawn
            };

            // Update the request status on the server
            axios.put(`http://127.0.0.1:5000/wfh_request/${this.selectedRequestId}`, payload)
                .then(() => {
                    // Update local state to reflect withdrawal
                    const index = this.your_requests.findIndex(request => request.request_id === this.selectedRequestId);
                    if (index !== -1) {
                        this.your_requests[index].status = 'Withdrawn'; // Update local status
                    }
                    window.alert('Request withdrawn successfully!');
                })
                .catch(error => {
                    console.error('Error withdrawing request:', error);
                    window.alert('Failed to withdraw request. Please try again.');
                });
        },
        confirmWithdrawal(requestId){
            console.log('byeeee')
            const payload = {
                status: 'Withdrawn'
            };

            // Make the API call to update the status in the backend
            axios.put(`http://127.0.0.1:5000/wfh_request/${requestId}`, payload)
                .then(() => {  
                })
                .catch(error => {
                    console.error('Error updating request:', error);
                    window.alert('Failed to approve request. Please try again.');
                    
                    // Optionally revert the optimistic update in case of an error
                    const index = this.your_requests.findIndex(request => request.request_id === requestId);
                    if (index !== -1) {
                        this.your_requests[index].status = 'Approved';  // Revert to approved
                    }
                });
        }
    },
    mounted() {
        this.employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
        this.populateWfhRequests()
        this.wfhRequest.staff_id = this.employee_obj.Staff_ID
    }
}

</script>

<style>
/* Add some basic styles for the toggle switch */
.switch {
    position: relative;
    display: inline-block;
    width: 40px; /* Adjust width */
    height: 20px; /* Adjust height */
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc; /* Default background */
    transition: .4s;
}

.slider:before {
    position: absolute;
    content: "";
    height: 16px; /* Adjust knob height */
    width: 16px; /* Adjust knob width */
    left: 2px; /* Adjust position */
    bottom: 2px; /* Adjust position */
    background-color: white;
    transition: .4s;
}

input:checked + .slider {
    background-color: #2196F3; /* Color when checked */
}

input:checked + .slider:before {
    transform: translateX(20px); /* Move knob when checked */
}

.slider.round {
    border-radius: 34px;
}

.slider.round:before {
    border-radius: 50%;
}

/* Optional: Adjust button styles */
/* .btn-secondary {
    width: 100%;
} */

/* Optional: Style for the multiselect */
.multiselect {
    border: 1px solid #ced4da; /* Default Bootstrap border */
    border-radius: 0.25rem; /* Bootstrap border-radius */
}
.toggle-text {
    margin-left: 10px; /* Adjust the value as needed for spacing */
}
.date-picker-box {
    border: 1px solid #ced4da; /* Default Bootstrap border */
    border-radius: 0.25rem; /* Bootstrap border-radius */
    padding: 10px; /* Add some padding */
    cursor: pointer; /* Change cursor to pointer */
    background-color: #f8f9fa; /* Light background */
}
</style>
