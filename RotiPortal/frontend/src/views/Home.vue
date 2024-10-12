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
                <!-- team schedule -->
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
            </ul>
        </div>

        <!-- Staff Dashboard -->
        <div v-if="activeTab === 'staff'" class="staff-dashboard">
            <div class="row align-items-start" style="margin-top: 150px;">
                <WFHRequestView />
            </div>
        </div>
        
        <!-- Own Schedule -->
        <div v-if="activeTab === 'schedule'" class="own-schedule">
            <div class="row align-items-start" style="margin-top: 120px;">
                <h2 class="mb-4">Own Schedule</h2>
                <ScheduleView />
            </div>
        </div>

        <!-- Manager View Team Schedule Dashboard -->
        <div v-if="activeTab === 'teamSchedule'" class="team-schedule">
            <div class="row align-items-start" style="margin-top: 160px;">
                <h2 class="mb-4">Team Schedule</h2>
                <TeamScheduleView />
            </div>
        </div>

        <!-- Manager Approval Dashboard -->
        <div v-if="activeTab === 'manager'" class="manager-dashboard">
            <div class="row align-items-start justify-content-center" style="margin-top: 150px;">
                <ManagerApprovalView />
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
import axios from 'axios';
import ScheduleView from '../components/ScheduleView.vue';
import TeamScheduleView from '../components/TeamScheduleView.vue';
import WFHRequestView from '../components/WFHRequestView.vue';
import ManagerApprovalView from '../components/ManagerApprovalView.vue';

export default {
    components: {
        WFHRequestView,
        ScheduleView,
        ManagerApprovalView,
        VDatePicker: DatePicker,
        ScheduleView,
        TeamScheduleView
    },
    data() {
        return {
            // general data
            employee_obj: {},
            role: 0,
            activeTab: 'staff',

            departmentBreakdown: [
                { name: 'Engineering', totalStaff: 20, inOffice: 15, wfh: 5, wfhPercentage: 25 },
                { name: 'Marketing', totalStaff: 15, inOffice: 10, wfh: 5, wfhPercentage: 33 },
                { name: 'Sales', totalStaff: 25, inOffice: 20, wfh: 5, wfhPercentage: 20 }
            ]

        }
    },
    computed: {},
    methods: {
        logout() {
            this.$router.push({ path: `/`, replace: true })
            sessionStorage.clear()
        },
    },
    mounted() {
        this.employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
        this.role = this.employee_obj.Role
    }
}
</script>

<style scoped>
/* Adjust card max-height for better visibility */
.card {
    max-height: calc(100vh - 250px);
    overflow-y: auto;
    scrollbar-width: none;
}
</style>