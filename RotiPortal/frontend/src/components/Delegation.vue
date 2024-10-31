<template>
    <div class="row mb-4 w-50">
        <div class="col-lg-6 mb-3">
            <!-- View Delegates Button -->
            <button class="btn btn-secondary w-100" data-bs-toggle="modal" data-bs-target="#viewDelegatesModal">
                View Current Delegates
            </button>
        </div>
        <div class="col-lg-6">
            <!-- Delegate Button -->
            <button class="btn btn-primary w-100" data-bs-toggle="modal" data-bs-target="#delegateModal">
                Delegate Authority
            </button>
        </div>

        <!-- View Delegates Modal -->
        <div class="modal fade" id="viewDelegatesModal" tabindex="-1" aria-labelledby="viewDelegatesModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="viewDelegatesModalLabel">Current Delegates</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Staff ID</th>
                                    <th>Name</th>
                                    <th>Start Date</th>
                                    <th>End Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="delegate in existingDelegates" :key="delegate.doc_id">
                                    <td>{{ delegate.delegate_id }}</td>
                                    <td>{{ fullName(delegate.delegate_id) }}</td>
                                    <td>{{ formatDateToDD_MMM_YYYY(delegate.start_date) }}</td>
                                    <td>{{ formatDateToDD_MMM_YYYY(delegate.end_date) }}</td>
                                    <td>
                                        <button class="btn btn-sm btn-danger" data-bs-dismiss="modal" data-bs-target="#revokeDelegationModal" @click="revokeDelegation(delegate.doc_id)">
                                            Revoke
                                        </button>
                                    </td>
                                </tr>
                                <tr v-if="existingDelegates.length === 0">
                                    <td colspan="5" class="text-center">No active delegates found</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Create Delegation Modal -->
        <div class="modal fade" id="delegateModal" tabindex="-1" aria-labelledby="delegateModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="delegateModalLabel">Delegate Authority</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="validateDelegation">
                            <div class="mb-3">
                                <label for="delegateSelect" class="form-label">Select Delegate</label>
                                <select class="form-select" id="delegateSelect" v-model="selectedDelegate" required>
                                    <option value="">Choose a delegate...</option>
                                    <option v-for="delegate in eligibleDelegates" 
                                            :key="delegate.Staff_ID" 
                                            :value="delegate.Staff_ID">
                                        {{ delegate.Staff_FName + " " + delegate.Staff_LName }}
                                    </option>
                                </select>
                            </div>
                            <div class="row">
                                <div class="col mb-3">
                                    <label for="startDate" class="form-label">Start Date</label>
                                    <v-date-picker v-model="startDate" class="form-control">
                                        <template v-slot="{ inputValue, inputEvents }">
                                            <input
                                                id="startDate"
                                                :value="inputValue"
                                                v-on="inputEvents"
                                                class="form-control"
                                                required
                                            />
                                        </template>
                                    </v-date-picker>
                                </div>
                                <div class="col-1 mx-0 d-flex align-items-center justify-content-center">
                                    <p class="text-center m-0">to</p>
                                </div>
                                <div class="col mb-3">
                                    <label for="endDate" class="form-label">End Date</label>
                                    <v-date-picker v-model="endDate" class="form-control">
                                        <template v-slot="{ inputValue, inputEvents }">
                                            <input
                                                id="endDate"
                                                :value="inputValue"
                                                v-on="inputEvents"
                                                class="form-control"
                                                required
                                            />
                                        </template>
                                    </v-date-picker>
                                </div>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Submit</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { DatePicker } from 'v-calendar';


export default {
    name: 'Delegation',
    components: {
        VDatePicker: DatePicker
    },
    data() {
        return {
            // general data
            employee_obj: {},
            employees: [],

            // delegation data
            selectedDelegate: 0,
            startDate: '',
            endDate: '',
            eligibleDelegates: [],
            existingDelegates: [],
        }
    },
    computed: {
        fullName() {
            return (staff_id) => {
                const thisEmployee = this.employees.find(employee => employee.Staff_ID === staff_id);
                if (!thisEmployee) return '';
                return `${thisEmployee.Staff_FName} ${thisEmployee.Staff_LName}`;
            }
        },
        eligibleDelegates() {
            return this.employees.filter(employee => employee.Role === 1 || employee.Role === 3)
        }
    },
    methods: {
        async fetchEmployees() {
            axios.get('http://127.0.0.1:5000/employee')
            .then(response => {
                this.employees = response.data
            })
            .catch(error => {
                console.log(error, "Error fetching employees")
            })
        },
        async fetchExistingDelegates() {
            axios.get('http://127.0.0.1:5000/delegate')
            .then(response => {
                this.existingDelegates = response.data
                console.log(this.existingDelegates)
            })
            .catch(error => {
                console.log(error, "Error fetching existing delegates")
            })
        },
        async validateDelegation() {
            if (this.startDate > this.endDate) {
                window.alert("Start date cannot be greater than end date!")
                return
            }
            // Check if delegate already exists
            const existingDelegate = this.existingDelegates.find(delegate => 
                delegate.delegate_id === this.selectedDelegate &&
                new Date(delegate.end_date) >= new Date()
            );
            
            if (existingDelegate) {
                window.alert("This person is already an active delegate!");
                return;
            }
            this.submitDelegation()
        },
        alertDelegate() {
            const payload = {
                staff_id:  this.employee_obj.Staff_ID,
                delegate_id: this.selectedDelegate,
                startDate: this.startDate,
                endDate: this.endDate
            };
            axios.post("http://127.0.0.1:5000/alert_delegate", payload)
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
        submitDelegation() {
            const delegateData = {
                    manager_id: this.employee_obj.Staff_ID,
                    delegate_id: this.selectedDelegate,
                    start_date: this.startDate,
                    end_date: this.endDate,
                    dept: this.employee_obj.Dept
                }
            axios.post('http://127.0.0.1:5000/delegate', delegateData)
            .then(response => {
                console.log(response.data)
                window.alert("Delegation created successfully!")
                this.alertDelegate()
                this.selectedDelegate = ''
                this.startDate = ''
                this.endDate = ''
                this.$forceUpdate()
                this.fetchExistingDelegates()
            })
            .catch(error => {
                console.log(error, "Error submitting delegation")
                window.alert("Error submitting delegation. Please try again.")
            })
        },
        formatDateToDD_MMM_YYYY(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
        },
        revokeDelegation(doc_id) {
            axios.delete(`http://127.0.0.1:5000/delegate/${doc_id}`)
            .then(response => {
                console.log(response.data)
                window.alert("Delegation revoked successfully!")
                this.fetchExistingDelegates()
                this.$forceUpdate()
            })
            .catch(error => {
                console.log(error, "Error revoking delegation")
                window.alert("Error revoking delegation. Please try again.")
            })
        }
    },
    mounted() {
        this.employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
        this.fetchEmployees()
        this.fetchExistingDelegates()
    }
}
</script>

<style scoped>
.modal-dialog {
    max-width: 500px;
}
</style>
