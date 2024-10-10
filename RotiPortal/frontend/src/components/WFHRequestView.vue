<template>
    <!-- Staff Dashboard -->
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
                            <option value="false">Non-Recurring</option>
                            <option value="true">Recurring</option>
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
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { DatePicker } from 'v-calendar';
import axios from 'axios'
export default {
    name: 'WFHRequestView',
    components: {
        VDatePicker: DatePicker
    },
    data() {
        return {
            employee_obj: {},
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
        }
    },
    computed: {
        sortedYourRequests() {
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Set to start of day for accurate comparison
        return [...this.your_requests]
            .filter(request => new Date(request.date) >= today)
            .sort((a, b) => new Date(a.date) - new Date(b.date));
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
                    this.$forceUpdate()
                    this.populateWfhRequests()
                }
            })
            .catch(error => {
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
        formatDateToDD_MMM_YYYY(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
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
</style>