<template>
    <div class="min-h-screen bg-gray-100 p-8">
      <div class="max-w-6xl mx-auto bg-white rounded-lg shadow-lg p-6">
        <h1 class="text-3xl font-bold mb-6 text-center text-gray-800">Team Schedule View</h1>
  
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
  
        <div class="mb-4">
          <label for="memberSelect" class="block text-sm font-medium text-gray-700 mb-2">Select Team Members:</label>
          <select
            id="memberSelect"
            v-model="selectedMembers"
            multiple
            class="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option v-for="member in teamMembers" :key="member" :value="member">
              {{ member }}
            </option>
          </select>
        </div>
  
        <div v-if="currentView === 'Monthly'" class="grid grid-cols-7 gap-1">
          <div v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="day" class="text-center font-bold p-2 bg-gray-100">
            {{ day }}
          </div>
          <div v-for="day in monthlyCalendar" :key="day.date.toISOString()" 
               class="border p-2 overflow-y-auto"
               :class="{'bg-gray-100': !day.isCurrentMonth}">
            <div class="font-semibold" :class="{'text-gray-400': !day.isCurrentMonth}">
              {{ day.date.getDate() }}
            </div>
            <div v-if="day.isCurrentMonth" class="text-xs">
              <template v-for="member in selectedMembers" :key="member">
                <div :class="getStatusClass(day, member, 'AM')">
                  {{ member }} AM: {{ getStatusText(day, member, 'AM') }}
                </div>
                <div :class="getStatusClass(day, member, 'PM')">
                  {{ member }} PM: {{ getStatusText(day, member, 'PM') }}
                </div>
              </template>
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
                <td class="border p-2">
                  <div v-for="member in selectedMembers" :key="`${member}-AM`" 
                       :class="getStatusClass(day, member, 'AM')"
                       class="p-1 mb-1 rounded">
                    <span class="font-semibold">{{ member }}:</span> {{ getStatusText(day, member, 'AM') }}
                  </div>
                </td>
                <td class="border p-2">
                  <div v-for="member in selectedMembers" :key="`${member}-PM`" 
                       :class="getStatusClass(day, member, 'PM')"
                       class="p-1 mb-1 rounded">
                    <span class="font-semibold">{{ member }}:</span> {{ getStatusText(day, member, 'PM') }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <div class="mt-6 flex justify-center space-x-4">
          <div v-for="(color, status) in statusColors" :key="status" class="flex items-center">
            <div :class="`w-4 h-4 rounded ${color} mr-2`"></div>
            <span class="text-sm text-gray-600">{{ status }}</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { ChevronLeftIcon, ChevronRightIcon, CalendarIcon } from 'lucide-vue-next'
  
  const views = ['Daily', 'Weekly', 'Monthly']
  const currentView = ref('Weekly')
  const currentDate = ref(new Date())
  const formattedDateForInput = ref(currentDate.value.toISOString().slice(0, 10))
  
  const teamMembers = ['Alice', 'Bob', 'Charlie']
  const selectedMembers = ref(['Alice'])
  
  const statusColors = {
    'Work from Office': 'bg-blue-200',
    'Work from Home Pending': 'bg-orange-200',
    'Work from Home Approved': 'bg-green-200',
    'Work from Home Rejected': 'bg-red-200',
    'On Leave': 'bg-gray-200'
  }
  
  const schedule = ref({
    'Alice': {
      'Mon Sep 02 2024': { AM: 'Work from Office', PM: 'Work from Office' },
      'Tue Sep 03 2024': { AM: 'Work from Home Pending', PM: 'Work from Office' },
      'Wed Sep 04 2024': { AM: 'Work from Office', PM: 'Work from Office' },
      'Thu Sep 05 2024': { AM: 'Work from Home Approved', PM: 'Work from Home Approved' },
      'Fri Sep 06 2024': { AM: 'Work from Home Rejected', PM: 'Work from Office' },
      'Sat Sep 07 2024': { AM: 'Work from Office', PM: 'On Leave' },
      'Sun Sep 08 2024': { AM: 'On Leave', PM: 'On Leave' },
    },
    'Bob': {
      'Mon Sep 02 2024': { AM: 'Work from Home Approved', PM: 'Work from Home Approved' },
      'Tue Sep 03 2024': { AM: 'Work from Office', PM: 'Work from Office' },
      'Wed Sep 04 2024': { AM: 'Work from Home Pending', PM: 'Work from Home Pending' },
      'Thu Sep 05 2024': { AM: 'Work from Office', PM: 'Work from Office' },
      'Fri Sep 06 2024': { AM: 'Work from Home Approved', PM: 'Work from Home Approved' },
      'Sat Sep 07 2024': { AM: 'On Leave', PM: 'On Leave' },
      'Sun Sep 08 2024': { AM: 'On Leave', PM: 'On Leave' },
    },
    'Charlie': {
      'Mon Sep 02 2024': { AM: 'Work from Office', PM: 'Work from Home Approved' },
      'Tue Sep 03 2024': { AM: 'Work from Home Pending', PM: 'Work from Home Rejected' },
      'Wed Sep 04 2024': { AM: 'Work from Office', PM: 'Work from Office' },
      'Thu Sep 05 2024': { AM: 'Work from Home Approved', PM: 'Work from Office' },
      'Fri Sep 06 2024': { AM: 'Work from Office', PM: 'Work from Home Pending' },
      'Sat Sep 07 2024': { AM: 'On Leave', PM: 'On Leave' },
      'Sun Sep 08 2024': { AM: 'On Leave', PM: 'On Leave' },
    }
  })
  
  const visibleDays = computed(() => {
    const days = []
    let start = new Date(currentDate.value)
    let end = new Date(currentDate.value)
  
    if (currentView.value === 'Daily') {
      end.setDate(start.getDate() + 1)
    } else if (currentView.value === 'Weekly') {
      start.setDate(start.getDate() - start.getDay())
      end.setDate(start.getDate() + 7)
    } else if (currentView.value === 'Monthly') {
      return [] // We'll use monthlyCalendar for the monthly view
    }
  
    for (let d = new Date(start); d < end; d.setDate(d.getDate() + 1)) {
      const dateString = d.toDateString()
      days.push({
        date: new Date(d),
        status: selectedMembers.value.reduce((acc, member) => {
          acc[member] = schedule.value[member][dateString] || { AM: 'No Status', PM: 'No Status' }
          return acc
        }, {})
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
        status: {}
      })
    }
  
    // Add days of current month
    for (let d = 1; d <= lastDay.getDate(); d++) {
      const date = new Date(year, month, d)
      const dateString = date.toDateString()
      days.push({
        date,
        isCurrentMonth: true,
        status: selectedMembers.value.reduce((acc, member) => {
          acc[member] = schedule.value[member][dateString] || { AM: 'No Status', PM: 'No Status' }
          return acc
        }, {})
      })
    }
  
    // Add padding days from next month
    for (let i = 1; i <= endPadding; i++) {
      const d = new Date(year, month + 1, i)
      days.push({
        date: d,
        isCurrentMonth: false,
        status: {}
      })
    }
  
    return days
  })
  
  const onDateChange = (e) => {
    const newDate = new Date(e.target.value)
    currentDate.value = newDate
  }
  
  const formattedDate = computed(() => {
    const options = { year: 'numeric', month: 'long' };
  
    if (currentView.value === 'Daily') {
      options.day = 'numeric';
      return currentDate.value.toLocaleDateString('en-US', options);
    }
  
    if (currentView.value === 'Weekly') {
      const startOfWeek = new Date(currentDate.value);
      const endOfWeek = new Date(startOfWeek);
      startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
      endOfWeek.setDate(startOfWeek.getDate() + 6);
  
      return `${startOfWeek.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })} - ${endOfWeek.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })}`;
    }
  
    return currentDate.value.toLocaleDateString('en-US', options);
  })
  
  const formatDay = (date) => {
    return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
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
  
  const getStatusClass = (day, member, period) => {
    const status = day.status[member]?.[period]
    return statusColors[status] || 'bg-gray-100'
  }
  
  const getStatusText = (day, member, period) => {
    return day.status[member]?.[period] || 'No Status'
  }
  </script>