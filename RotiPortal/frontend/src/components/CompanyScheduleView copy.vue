<template>
    <div class="min-h-screen">
      <div class="max-w-6xl mx-auto bg-white rounded-lg border-1 p-6">  
        <div class="mb-6 flex justify-between items-center">
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
          <div class="flex space-x-4 items-center">  
            <button @click="changeDate(-1)" class="text-gray-600 hover:text-gray-800">
              <ChevronLeftIcon class="h-6 w-6" />
            </button>
            <span class="text-lg font-semibold">{{ formattedDate }}</span>
  
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
  
            <button @click="changeDate(1)" class="text-gray-600 hover:text-gray-800">
              <ChevronRightIcon class="h-6 w-6" />
            </button>
          </div>
        </div>
  
        <div v-if="currentView === 'Monthly'" class="grid grid-cols-7 gap-1">
          <div v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="day" class="text-center font-bold p-2 bg-gray-100">
            {{ day }}
          </div>
          <div v-for="day in monthlyCalendar" :key="day.date" 
               class="border p-2 overflow-y-auto"
               :class="{'bg-gray-100': !day.isCurrentMonth}">
            <div class="font-semibold" :class="{'text-gray-400': !day.isCurrentMonth}">
              {{ day.date.getDate() }}
            </div>
            <div v-if="day.isCurrentMonth" class="text-xs">
              <!-- <div :class="getStatusClass(day, 'AM')">AM: {{ getStatusText(day, 'AM') }}</div> -->
              <!-- <div :class="getStatusClass(day, 'PM')">PM: {{ getStatusText(day, 'PM') }}</div> -->
            </div>
          </div>
        </div>
  
        <div v-else class="overflow-x-auto">
          <table class="w-full border-collapse">
            <thead>
              <tr>
                <th class="border p-2 bg-gray-100">Date</th>
                <th class="border p-2 bg-gray-100">AM</th>
                <th class="border p-2 bg-gray-100">PM</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in approvedRequests" :key="request.date">
                <td class="border p-2">{{ formatDay(request.date) }}</td>
                <!-- <td class="border p-2" :class="getStatusClass(day, 'AM')"> -->
                <!-- </td> -->
                <td class="border p-2">
                    <div class="progress" role="progressbar" aria-label="Basic example">
                        <div class="progress-bar" :style="{width: getWFOPercentage(request.date, 'AM')}"></div>
                    </div>
                </td>
                  <!-- {{ getStatusText(day, 'AM') }} -->
                <td class="border p-2">
                  <!-- {{ getStatusText(day, 'PM') }} -->
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
<script>
import { ChevronLeftIcon, ChevronRightIcon, CalendarIcon } from 'lucide-vue-next'
import axios from 'axios'

export default {
    name: 'CompanyScheduleView',
    data() {
        return {
            // ui
            views: ['Daily', 'Weekly', 'Monthly'],
            currentView: 'Weekly',
            currentDate: new Date(),
            formattedDateForInput: new Date().toISOString().slice(0, 10),

            // general
            employee_obj: {},
            staff_id: '',

            // company schedule data
            employees: [],
            approvedRequests: []
        }
    },
    computed: {
        visibleDays() {
            if (this.currentView === 'Monthly') {
                return [] // Use monthlyCalendar for monthly view
            }
        
            const days = []
            let start = new Date(this.currentDate)
            let end = new Date(this.currentDate)
        
            if (this.currentView === 'Daily') {
                end.setDate(start.getDate() + 1)
            } else if (this.currentView === 'Weekly') {
                start.setDate(start.getDate() - start.getDay())
                end.setDate(start.getDate() + 7)
            }
        
            for (let d = new Date(start); d < end; d.setDate(d.getDate() + 1)) {
                const dateString = d.toDateString()
                days.push({
                    date: new Date(d),
                    // status: this.schedule[dateString] || { AM: { arrangement: 'No Status', status: 'No Status' }, PM: { arrangement: 'No Status', status: 'No Status' } }
                })
            }
        
            return days
        },
        monthlyCalendar() {
          const year = this.currentDate.getFullYear()
          const month = this.currentDate.getMonth()
          const firstDay = new Date(year, month, 1)
          const lastDay = new Date(year, month + 1, 0)
          
          const days = []
          const startPadding = firstDay.getDay()
          const endPadding = 6 - lastDay.getDay()
        
          // Add padding days from previous month
          for (let i = startPadding - 1; i >= 0; i--) {
            const d = new Date(year, month, -i)
            days.push({
              date: d,
              isCurrentMonth: false,
            //   status: { AM: { arrangement: 'No Status', status: 'No Status' }, PM: { arrangement: 'No Status', status: 'No Status' } }
            })
          }
        
          // Add days of current month
          for (let d = 1; d <= lastDay.getDate(); d++) {
            const date = new Date(year, month, d)
            const dateString = date.toDateString()
            days.push({
              date,
              isCurrentMonth: true,
            //   status: this.schedule[dateString] || { AM: { arrangement: 'No Status', status: 'No Status' }, PM: { arrangement: 'No Status', status: 'No Status' } }
            })
          }
        
          // Add padding days from next month
          for (let i = 1; i <= endPadding; i++) {
            const d = new Date(year, month + 1, i)
            days.push({
              date: d,
              isCurrentMonth: false,
            //   status: { AM: { arrangement: 'No Status', status: 'No Status' }, PM: { arrangement: 'No Status', status: 'No Status' } }
            })
          }
        
          return days
        },
        formattedDate() {
            const options = { year: 'numeric', month: 'long' }
        
            if (this.currentView === 'Daily') {
                options.day = 'numeric'
                return this.currentDate.toLocaleDateString('en-US', options)
            }
        
            if (this.currentView === 'Weekly') {
                const startOfWeek = new Date(this.currentDate)
                const endOfWeek = new Date(startOfWeek)
                startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay())
                endOfWeek.setDate(startOfWeek.getDate() + 6)
        
                return `${startOfWeek.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })} - ${endOfWeek.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })}`
            }
        
            return this.currentDate.toLocaleDateString('en-US', options)
        }
        // schedule() {
           //     const map = {};
           //     this.scheduleData.forEach(entry => {
           //         const dateStr = new Date(entry.Date).toDateString();
   
           //         if (!map[dateStr]) {
           //             map[dateStr] = { AM: { arrangement: 'No Status', status: 'No Status' }, PM: { arrangement: 'No Status', status: 'No Status' } };
           //         }
   
           //         const period = entry.Duration === 'FD' ? ['AM', 'PM'] : [entry.Duration];
           //         period.forEach(p => {
           //             map[dateStr][p] = { arrangement: entry.Work_Arrangement, status: entry.Status };
           //         });
           //     });
           //     return map;
           // },
    },
    methods: {
        getEmployees() {
            axios.get('http://127.0.0.1:5000/employee')
            .then(response => {
                this.employees = response.data
            })
            .catch(error => {
                console.error('Error fetching employees:', error)
            })
        },
        // get company schedule
        getApprovedRequests() {
            axios.get('http://127.0.0.1:5000/wfh_request')
            .then(response => {
                const allRequests = response.data
                for (const request of allRequests) {
                    if (request.status == 'Approved') {
                        this.approvedRequests.push(request)
                    }
                }
                console.log(this.approvedRequests)
            })
            .catch(error => {
                console.error('Error fetching requests data:', error)
            })
        },
        getWFOPercentage(date, shift) {
            const numOfWfh = 0
            for (const request of this.approvedRequests) {
                if (request.date == date && request.shift == shift) {
                    numOfWfh += 1
                }
            }
            return (1- (numOfWfh/this.employees.length) * 100).toFixed(0) + '%'
        },
        onDateChange(e) {
            const newDate = new Date(e.target.value)
            this.currentDate = newDate
        },
        
        formatDay(date) {
            return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
        },
        
        changeDate(delta) {
            const newDate = new Date(this.currentDate)
            if (this.currentView === 'Daily') {
                newDate.setDate(newDate.getDate() + delta)
            } else if (this.currentView === 'Weekly') {
                newDate.setDate(newDate.getDate() + delta * 7)
            } else if (this.currentView === 'Monthly') {
                newDate.setMonth(newDate.getMonth() + delta)
            }
            this.currentDate = newDate
            this.formattedDateForInput = this.currentDate.toISOString().slice(0, 10)
        },
        
        getStatusClass(day, period) {
            const arrangement = day.status[period]?.arrangement || 'No Status';
            const status = day.status[period]?.status || 'No Status';
            return this.statusColors[arrangement]?.[status] || 'bg-gray-100';
        },

        getStatusText(day, period) {
            const arrangement = day.status[period]?.arrangement || 'No Status';
            const status = day.status[period]?.status || 'No Status';
            return `${arrangement}`;
        }
    },
    mounted() {
        this.employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
        this.staff_id = this.employee_obj.Staff_ID
        this.getApprovedRequests()
    },
}
</script>