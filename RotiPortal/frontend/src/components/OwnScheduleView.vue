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
              <div :class="getStatusClass(day, 'AM')">AM: {{ getStatusText(day, 'AM') }}</div>
              <div :class="getStatusClass(day, 'PM')">PM: {{ getStatusText(day, 'PM') }}</div>
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
              <tr v-for="day in visibleDays" :key="day.date">
                <td class="border p-2">{{ formatDay(day.date) }}</td>
                <td class="border p-2" :class="getStatusClass(day, 'AM')">
                  {{ getStatusText(day, 'AM') }}
                </td>
                <td class="border p-2" :class="getStatusClass(day, 'PM')">
                  {{ getStatusText(day, 'PM') }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-5 flex justify-center space-x-4">
          <div :class="`w-4 h-4 rounded bg-blue-200 mr-2`"></div>
          <span class="text-sm text-gray-600">Work from Office</span>
          <div :class="`w-4 h-4 rounded bg-green-200 mr-2`"></div>
          <span class="text-sm text-gray-600">Work from Home Approved</span>
          <div :class="`w-4 h-4 rounded bg-orange-200 mr-2`"></div>
          <span class="text-sm text-gray-600">Work from Home Pending</span>
          <div :class="`w-4 h-4 rounded bg-red-200 mr-2`"></div>
          <span class="text-sm text-gray-600">Work from Home Rejected</span>
          <div :class="`w-4 h-4 rounded bg-gray-400 mr-2`"></div>
          <span class="text-sm text-gray-600">On Leave</span>
          <div :class="`w-4 h-4 rounded bg-gray-100 mr-2`"></div>
          <span class="text-sm text-gray-600">No Status</span>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { ChevronLeftIcon, ChevronRightIcon, CalendarIcon } from 'lucide-vue-next'
  import { DatePicker } from 'v-calendar';
  import axios from 'axios'
  
  const views = ['Daily', 'Weekly', 'Monthly']
  const currentView = ref('Weekly')
  const currentDate = ref(new Date())
  const formattedDateForInput = ref(currentDate.value.toISOString().slice(0, 10))
  
  let employee_obj = ref(null);
  let staff_id = ref("");
  
  // Update statusColors to map work arrangement to color classes
  const statusColors = {
    'Work from Office': {
      'Approved': 'bg-blue-200',
    },
    'Work from Home': {
      'Approved': 'bg-green-200',
      'Pending': 'bg-orange-200',
      'Rejected': 'bg-red-200',
    },
    'On Leave': {
      'Approved': 'bg-gray-400',
    },
    'No Status': {
      '': 'bg-gray-100',
    },
  };

  // Adjusted schedule data to match the new structure
  const scheduleData = ref([]);

  onMounted(async () => {
    try {
      employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"))
      staff_id = employee_obj.Staff_ID
      const response = await axios.get('https://spm-roti-prata.onrender.com/wfh_request/staff/' + staff_id)
      scheduleData.value = response.data
    } catch (error) {
      console.error('Error fetching schedule data:', error)
    }
  })
  
  // Function to convert scheduleData into a mapping for easier access
  const schedule = computed(() => {
    const map = {};
    scheduleData.value.forEach(entry => {
      const dateStr = new Date(entry.date).toDateString();

      if (!map[dateStr]) {
        map[dateStr] = { AM: { arrangement: 'Work from Office', status: 'Approved' }, PM: { arrangement: 'Work from Office', status: 'Approved' } };
      }

      const period = entry.shift === 'FD' ? ['AM', 'PM'] : [entry.shift];

      const arrangement = (entry.status === 'Withdrawn' || entry.status === 'Cancelled')
      ? { arrangement: 'Work from Office', status: 'Approved' }
      : { arrangement: 'Work from Home', status: entry.status };

      period.forEach(p => {
        map[dateStr][p] = arrangement;
      });
    });
    return map;
  });

  const visibleDays = computed(() => {
    if (currentView.value === 'Monthly') {
      return [] // Use monthlyCalendar for monthly view
    }
  
    const days = []
    let start = new Date(currentDate.value)
    let end = new Date(currentDate.value)

    if (currentView.value === 'Daily') {
      end.setDate(start.getDate() + 1);
    } else if (currentView.value === 'Weekly') {
      start.setDate(start.getDate() - start.getDay()); // Set start to the Sunday of the current week
      end = new Date(start); // Reset the end to start
      end.setDate(start.getDate() + 7); // Set end to the Saturday of the same week
    }

    for (let d = new Date(start); d < end; d.setDate(d.getDate() + 1)) {
      const dateString = d.toDateString()

      days.push({
        date: new Date(d),
        status: schedule.value[dateString] || { AM: 'No Status', PM: 'No Status' }
      })
    }
  
    return days
  })
  
  const monthlyCalendar = computed(() => {
    const year = currentDate.value.getFullYear()
    const month = currentDate.value.getMonth()
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
        status: { AM: 'No Status', PM: 'No Status' }
      })
    }
  
    // Add days of current month
    for (let d = 1; d <= lastDay.getDate(); d++) {
      const date = new Date(year, month, d)
      const dateString = date.toDateString()

      days.push({
        date,
        isCurrentMonth: true,
        status: schedule.value[dateString] || { AM: 'No Status', PM: 'No Status' }
      })
    }
  
    // Add padding days from next month
    for (let i = 1; i <= endPadding; i++) {
      const d = new Date(year, month + 1, i)
      days.push({
        date: d,
        isCurrentMonth: false,
        status: { AM: 'No Status', PM: 'No Status' }
      })
    }
  
    return days
  })
  
  const onDateChange = (e) => {
    const newDate = new Date(e.target.value)
    currentDate.value = newDate
  }

  const formattedDate = computed(() => {
    const options = { year: 'numeric', month: 'long' }
  
    if (currentView.value === 'Daily') {
      options.day = 'numeric'
      return currentDate.value.toLocaleDateString('en-SG', options)
    }
  
    if (currentView.value === 'Weekly') {
      const startOfWeek = new Date(currentDate.value)
      startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay())  // Calculate startOfWeek first

      const endOfWeek = new Date(startOfWeek)  // Create endOfWeek after startOfWeek is finalized
      endOfWeek.setDate(startOfWeek.getDate() + 6)  // Set endOfWeek correctly
      
      return `${startOfWeek.toLocaleDateString('en-SG', { month: 'long', day: 'numeric' })} - ${endOfWeek.toLocaleDateString('en-SG', { month: 'long', day: 'numeric' })}`
    }
  
    return currentDate.value.toLocaleDateString('en-SG', options)
  })
  
  const formatDay = (date) => {
    return date.toLocaleDateString('en-SG', { weekday: 'short', month: 'short', day: 'numeric' })
  }
  
  const changeDate = (delta) => {
    const newDate = new Date(currentDate.value)
    if (currentView.value === 'Daily') {
      newDate.setDate(newDate.getDate() + delta)
    } else if (currentView.value === 'Weekly') {
      newDate.setDate(newDate.getDate() + delta * 7)
    } else if (currentView.value === 'Monthly') {
      newDate.setMonth(newDate.getMonth() + delta)
    }
    currentDate.value = newDate
    formattedDateForInput.value = currentDate.value.toISOString().slice(0, 10)
  }
  
  const getStatusClass = (day, period) => {
    const arrangement = day.status[period]?.arrangement || 'Work from Office';
    const status = day.status[period]?.status || 'Approved';
    return statusColors[arrangement]?.[status] || 'bg-blue-200';
  };

  const getStatusText = (day, period) => {
    const arrangement = day.status[period]?.arrangement || 'Work from Office';
    return `${arrangement}`;
  };

  defineExpose({ DatePicker });
  </script>