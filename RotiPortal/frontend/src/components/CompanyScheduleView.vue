<template>
    <div class="min-h-screen">
        <div class="w-100 mx-auto bg-white rounded-lg border-1 p-6">
            <div class="mb-6 flex justify-between items-center">

                <!-- View Buttons -->
                <div class="space-x-2">
                    <button
                        v-for="view in views"
                        :key="view"
                        @click="currentView = view"
                        class="px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150"
                        :class="currentView === view ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
                    >
                        {{ view }}
                    </button>
                </div>

                <!-- Date Picker -->
                <div class="d-flex gap-2 items-center">
                    <!-- Left Arrow -->
                    <button @click="changeDate(-1)" class="text-gray-600 hover:text-gray-800">
                        <ChevronLeftIcon class="h-6 w-6" />
                    </button>
                    <span class="text-lg font-semibold">{{ formattedDate }}</span>
        
                    <!-- Date Picker -->
                    <div class="relative">
                        <input 
                            type="date" 
                            v-model="formattedDateForInput" 
                            @change="onDateChange" 
                            class="absolute inset-0 opacity-0 cursor-pointer" 
                            ref="dateInput" 
                        />
                        <button @click="$refs.dateInput.click()" class="text-gray-600 hover:text-gray-800">
                            <CalendarIcon class="h-6 w-6" />
                        </button>
                    </div>
        
                    <!-- Right Arrow -->
                    <button @click="changeDate(1)" class="text-gray-600 hover:text-gray-800">
                        <ChevronRightIcon class="h-6 w-6" />
                    </button>
                </div>
            </div>

            <!-- Display -->
            <!-- Daily view -->
            <div v-if="currentView === 'Day'" class="w-100">
                <table class="w-full border-collapse">
                    <thead>
                        <tr>
                            <th class="border p-2 bg-gray-100" rowspan="2">Date</th>
                            <th class="border p-2 bg-gray-100" colspan="2">Percentage of Employees in Office</th>
                        </tr>
                        <tr>
                            <th class="border p-2 bg-gray-100">AM</th>
                            <th class="border p-2 bg-gray-100">PM</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <!-- date -->
                            <td class="border p-2" style="width: 33%;">{{ formatDateToDD_MMM_YYYY(currentDate) }}</td>
                            <!-- AM -->
                            <td class="border p-2 hoverable-cell" style="width: 33%;" data-bs-toggle="modal" data-bs-target="#WfhModal" @click="viewModal(currentDate, 'AM')">
                                <div class="progress" role="progressbar">
                                    <div class="progress-bar" 
                                        :class="{
                                            'bg-success': getWFOPercentage(currentDate, 'AM') > 75,
                                            'bg-warning': getWFOPercentage(currentDate, 'AM') > 25 && getWFOPercentage(currentDate, 'AM') <= 75,
                                            'bg-danger': getWFOPercentage(currentDate, 'AM') <= 25
                                        }"
                                        :style="{width: getWFOPercentage(currentDate, 'AM') + '%'}">
                                    </div>
                                </div>
                                <span class="text-sm">{{ getWFOPercentage(currentDate, 'AM') }}%</span>
                            </td>
                            <!-- PM -->
                            <td class="border p-2 hoverable-cell" style="width: 33%;" data-bs-toggle="modal" data-bs-target="#WfhModal" @click="viewModal(currentDate, 'PM')">
                                <div class="progress" role="progressbar">
                                    <div class="progress-bar" 
                                        :class="{
                                            'bg-success': getWFOPercentage(currentDate, 'PM') > 75,
                                            'bg-warning': getWFOPercentage(currentDate, 'PM') > 25 && getWFOPercentage(currentDate, 'PM') <= 75,
                                            'bg-danger': getWFOPercentage(currentDate, 'PM') <= 25
                                        }"
                                        :style="{width: getWFOPercentage(currentDate, 'PM') + '%'}">
                                    </div>
                                </div>
                                <span class="text-sm">{{ getWFOPercentage(currentDate, 'PM') }}%</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Weekly view -->
            <div v-if="currentView === 'Week'" class="w-100">
                <table class="w-full border-collapse">
                    <thead>
                        <tr>
                            <th class="border p-2 bg-gray-100" rowspan="2">Date</th>
                            <th class="border p-2 bg-gray-100" colspan="2">Percentage of Employees in Office</th>
                        </tr>
                        <tr>
                            <th class="border p-2 bg-gray-100">AM</th>
                            <th class="border p-2 bg-gray-100">PM</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="date in visibleWeekDates" :key="date">
                            <!-- Date -->
                            <td class="border p-2" style="width: 33%;">{{ formatDateToDD_MMM_YYYY(date) }}</td>
                            <!-- AM -->
                            <td class="border p-2 hoverable-cell" style="width: 33%;" data-bs-toggle="modal" data-bs-target="#WfhModal" @click="viewModal(date, 'AM')">
                                <div class="progress" role="progressbar">
                                    <div class="progress-bar" 
                                        :class="{
                                            'bg-success': getWFOPercentage(date, 'AM') > 75,
                                            'bg-warning': getWFOPercentage(date, 'AM') > 25 && getWFOPercentage(date, 'AM') <= 75,
                                            'bg-danger': getWFOPercentage(date, 'AM') <= 25
                                        }"
                                        :style="{width: getWFOPercentage(date, 'AM') + '%'}">
                                    </div>
                                </div>
                                <span class="text-sm">{{ getWFOPercentage(date, 'AM') }}%</span>
                            </td>
                            <!-- PM -->
                            <td class="border p-2 hoverable-cell" style="width: 33%;" data-bs-toggle="modal" data-bs-target="#WfhModal" @click="viewModal(date, 'PM')">
                                <div class="progress" role="progressbar">
                                    <div class="progress-bar" 
                                        :class="{
                                            'bg-success': getWFOPercentage(date, 'PM') > 75,
                                            'bg-warning': getWFOPercentage(date, 'PM') > 25 && getWFOPercentage(date, 'PM') <= 75,
                                            'bg-danger': getWFOPercentage(date, 'PM') <= 25
                                        }"
                                        :style="{width: getWFOPercentage(date, 'PM') + '%'}">
                                    </div>
                                </div>
                                <span class="text-sm">{{ getWFOPercentage(date, 'PM') }}%</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Monthly view -->
            <div v-if="currentView === 'Month'" class="w-100">
                <table class="w-full border-collapse">
                    <thead>
                        <tr>
                            <th class="border p-2 bg-gray-100" style="width: 14.3%;">Sun</th>
                            <th class="border p-2 bg-gray-100" style="width: 14.3%;">Mon</th>
                            <th class="border p-2 bg-gray-100" style="width: 14.3%;">Tue</th>
                            <th class="border p-2 bg-gray-100" style="width: 14.3%;">Wed</th>
                            <th class="border p-2 bg-gray-100" style="width: 14.3%;">Thu</th>
                            <th class="border p-2 bg-gray-100" style="width: 14.3%;">Fri</th>
                            <th class="border p-2 bg-gray-100" style="width: 14.3%;">Sat</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="week in visibleMonthDates" :key="week[0]">
                            <td v-for="date in week" :key="date" class="border p-2 text-center hoverable-cell" style="width: 92.3px;" data-bs-toggle="modal" data-bs-target="#WfhModal" @click="viewModal(date, '')">
                                <span style="font-weight: bold;">{{ date ? date.getDate() : '' }}</span>
                                <template v-if="date">
                                    <div class="progress" role="progressbar">
                                        <div class="progress-bar" 
                                            :class="{
                                                'bg-success': getWFOPercentage(date, '') > 75,
                                                'bg-warning': getWFOPercentage(date, '') > 25 && getWFOPercentage(date, '') <= 75,
                                                'bg-danger': getWFOPercentage(date, '') <= 25
                                            }"
                                            :style="{width: getWFOPercentage(date, '') + '%'}">
                                        </div>
                                    </div>
                                    <span class="text-sm">{{ getWFOPercentage(date, '') }}%</span>
                                </template>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- WFH Modal -->
             <div id="WfhModal" class="modal" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">{{ selectedDate.date }} <span class="ms-3 fw-bold">{{ selectedDate.shift }}</span></h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <table class="table table-striped text-center">
                                <thead>
                                    <tr>
                                        <th>Work from Office</th>
                                        <th>Work from Home</th>
                                    </tr>
                                </thead>
                                <tbody>
                                   <tr>
                                        <td>
                                            <ul>
                                                <li v-for="employee in selectedDate.employees.wfo" :key="employee">{{ employee }}</li>
                                            </ul>
                                        </td>
                                        <td>
                                            <ul>
                                                <li v-for="employee in selectedDate.employees.wfh" :key="employee">{{ employee }}</li>
                                            </ul>
                                        </td>
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
import { ChevronLeftIcon, ChevronRightIcon, CalendarIcon } from 'lucide-vue-next';

export default {
    name: 'CompanyScheduleView',
    components: {
        ChevronLeftIcon, ChevronRightIcon, CalendarIcon
    },
    data() {
        return {
            // component data
            views: ['Day', 'Week', 'Month'],
            currentView: 'Week',
            approvedRequests: [],

            // general data
            currentDate: this.getTodaysDate(),
            employees: [],

            // modal data
            selectedDate: {
                date: '',
                shift: '',
                employees: {
                    wfh: [],
                    wfo: []
                }
            },

            // date picker data
            formattedDateForInput: this.getTodaysDate().toISOString().slice(0, 10)
        };
    },
    computed: {
        visibleWeekDates() {
            const today = new Date(this.currentDate);
            const dayOfWeek = today.getDay();
            const diff = today.getDate() - dayOfWeek; // Start from Sunday
            const sunday = new Date(today.setDate(diff));
            
            const weekDates = [];
            for (let i = 0; i < 7; i++) { // 7 days of the week
                const date = new Date(sunday);
                date.setDate(sunday.getDate() + i);
                weekDates.push(date);
            }
            
            return weekDates;
        },
        visibleMonthDates() {
            const year = this.currentDate.getFullYear();
            const month = this.currentDate.getMonth();
            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            
            const daysInMonth = lastDay.getDate();
            const startingDayOfWeek = firstDay.getDay();
            
            const calendar = [];
            let day = 1;
            
            for (let i = 0; i < 6; i++) {
                const week = [];
                for (let j = 0; j < 7; j++) {
                    if (i === 0 && j < startingDayOfWeek) {
                        week.push(null);
                    } else if (day > daysInMonth) {
                        week.push(null);
                    } else {
                        week.push(new Date(year, month, day));
                        day++;
                    }
                }
                calendar.push(week);
                if (day > daysInMonth) break;
            }
            
            return calendar;
        },
        formattedDate() {
            const options = { year: 'numeric', month: 'long' };
  
            if (this.currentView === 'Day') {
                options.day = 'numeric';
                return this.currentDate.toLocaleDateString('en-US', options);
            }
  
            if (this.currentView === 'Week') {
                const startOfWeek = new Date(this.currentDate);
                const endOfWeek = new Date(startOfWeek);
                startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
                endOfWeek.setDate(startOfWeek.getDate() + 6);
  
                return `${startOfWeek.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })} - ${endOfWeek.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })}`;
            }
  
            return this.currentDate.toLocaleDateString('en-US', options);
        },
    },
    methods: {
        getTodaysDate() {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            return today;
        },
        getEmployees() {
            axios.get("http://127.0.0.1:5000/employee")
            .then((response) => {
                this.employees = response.data;
            })
            .catch((error) => {
                console.error("Error fetching employees:", error);
            });
        },
        getApprovedRequests() {
            axios.get("http://127.0.0.1:5000/wfh_request")
            .then((response) => {
                const allRequests = response.data;
                for (const request of allRequests) {
                    if (request.status === 'Approved') {
                        this.approvedRequests.push(request);
                    }
                }
            })
            .catch((error) => {
                console.error("Error fetching approved requests:", error);
            });
        },
        formatDateToDD_MMM_YYYY(dateString) {
            const date = new Date(dateString);
            const options = { 
                weekday: 'short', // This adds the short name of the day
                day: '2-digit', 
                month: 'short', 
                year: 'numeric' 
            };
            return date.toLocaleDateString('en-GB', options);
        },
        onDateChange(e) {
            const newDate = new Date(e.target.value);
            this.currentDate = newDate;
        },
        getWFOPercentage(date, shift) {
            if (!(date instanceof Date)) {
                date = new Date(date);
            }
            var numOfWfhEmployees = 0

            if (shift === 'AM' || shift === 'PM') {
                for (const request of this.approvedRequests) {
                    if (request.date == date.toISOString() && (request.shift === shift || request.shift === 'FD')) {
                        numOfWfhEmployees += 1;
                    }
                }
            } else if (shift === '') {
                for (const request of this.approvedRequests) {
                    if (request.date == date.toISOString() && (request.shift === 'AM' || request.shift === 'PM' || request.shift === 'FD')) {
                        numOfWfhEmployees += 1;
                    }
                }
            }
            return ((1 - numOfWfhEmployees / this.employees.length) * 100).toFixed(0);
        },
        viewModal(date, shift) {
            if (!(date instanceof Date)) {
                date = new Date(date);
            }
            const wfhEmployees = [];
            const wfoEmployees = [];
            const wfhStaffID = [];
            
            // Filter approved requests for the given date and shift
            if (shift === 'AM' || shift === 'PM') {
                for (const request of this.approvedRequests) {
                    if (request.date === date.toISOString() && (request.shift === shift || request.shift === 'FD')) {
                        wfhStaffID.push(request.staff_id);
                    }
                }
            } else if (shift === '') {
                for (const request of this.approvedRequests) {
                    if (request.date === date.toISOString() && (request.shift === 'AM' || request.shift === 'PM' || request.shift === 'FD')) {
                        wfhStaffID.push(request.staff_id);
                    }
                }
            }

            for (const employee of this.employees) {
                if (wfhStaffID.includes(employee.Staff_ID)) {
                    wfhEmployees.push(employee.Staff_FName + " " + employee.Staff_LName);
                } else {
                    wfoEmployees.push(employee.Staff_FName + " " + employee.Staff_LName);
                }
            }

            // Set the selectedDate object
            this.selectedDate = {
                date: this.formatDateToDD_MMM_YYYY(date),
                shift: shift,
                employees: {
                    wfh: wfhEmployees,
                    wfo: wfoEmployees
                }
            };
        },
        changeDate(delta) {
            const newDate = new Date(this.currentDate);
            if (this.currentView === 'Day') {
                newDate.setDate(newDate.getDate() + delta);
            } else if (this.currentView === 'Week') {
                newDate.setDate(newDate.getDate() + delta * 7);
            } else if (this.currentView === 'Month') {
                newDate.setMonth(newDate.getMonth() + delta);
            }
            this.currentDate = newDate;
            this.formattedDateForInput = this.currentDate.toISOString().slice(0, 10);
        }
    },
    mounted() {
        this.getApprovedRequests();
        this.getEmployees();
    },
};
</script>

<style scoped>
.hoverable-cell {
    cursor: pointer;
}
</style>
