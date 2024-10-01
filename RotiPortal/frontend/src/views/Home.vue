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
                    <a class="nav-link" :class="{ active: activeTab === 'teamSchedule' }" href="#"
                        @click.prevent="activeTab = 'teamSchedule'">Team Schedule</a>
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
                                        <label for="recurring" class="form-label">Arrangement</label>
                                        <select name="recurring" id="recurring" v-model="wfhRequest.recurring" class="form-select">
                                            <option value="true">Recurring</option>
                                            <option value="false">Non-Recurring</option>
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

        <!-- Manager Approval Dashboard -->
        <div v-if="activeTab === 'manager'">
            <div class="row align-items-start" style="margin-top: -130px;">
                <h2>Manager Approval Dashboard</h2>
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
                                <tr v-for="request in pendingRequests" :key="request.id">
                                    <td>{{ request.employee }}</td>
                                    <td>{{ request.type }}</td>
                                    <td>{{ request.date }}</td>
                                    <td>
                                        <button @click="approveRequest(request.id)"
                                            class="btn btn-sm btn-success me-2">Approve</button>
                                        <button @click="rejectRequest(request.id)"
                                            class="btn btn-sm btn-danger">Reject</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
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
export default {
    components: {
        VDatePicker: DatePicker
    },
    data() {
        return {
            employees: [],
            isLoading: true,
            employee_obj: {},
            role: 0,
            activeTab: 'staff',
            wfhRequest: {
                date: '',
                reason: '',
                recurring: false,
                attachments: null
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
            ]
        }
    },
    methods: {
        submitWfhRequest() {
            // Logic to submit WFH request
            console.log('Submitting WFH request:', this.wfhRequest)
            axios.post("http://localhost:5000/wfh_request", this.wfhRequest)
            .then(response => {
                console.log(response)
            })
            .catch(error => {
                console.log(error)
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
                console.log(fetchedEmployees)
            } catch (error) {
                console.error("Error getting documents: ", error)
            }
        },
    },
    mounted() {
        this.employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
        this.role = this.employee_obj.Role
        setTimeout(() => {
        // Once data is loaded, set isLoading to false
        this.fetchEmployeeData() // Fetch employee when the component is mounted
        }, 500)
    }
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>