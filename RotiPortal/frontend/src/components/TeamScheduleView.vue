<template>
  <div class="min-h-screen">
    <div class="max-w-6xl mb-auto bg-white rounded-lg border-1 p-6">
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
        <label class="block text-sm font-medium text-gray-700 mb-2">Select Team Members:</label>
        <div class="relative">
          <button @click="toggleDropdown" class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-left">
            {{ selectedMembers.length }} member(s) selected
          </button>
          <div v-if="isDropdownOpen" class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
            <div v-for="member in teamMembers" :key="member" class="px-3 py-2">
              <label class="flex items-center">
                <input type="checkbox" v-model="selectedMembers" :value="member" class="mr-2">
                {{ member }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <div v-if="currentView === 'Monthly'" class="grid grid-cols-7 gap-1">
        <div v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="day" class="text-center font-bold p-2 bg-gray-100">
          {{ day }}
        </div>
        <div v-for="day in monthlyCalendar" :key="day.date.toISOString()" 
             class="border p-2 overflow-y-auto cursor-pointer"
             :class="[{'bg-gray-100': !day.isCurrentMonth}, getDayBackgroundColor(day)]"
             @click="openModal(day)">
          <div class="font-semibold" :class="{'text-gray-400': !day.isCurrentMonth}">
            {{ day.date.getDate() }}
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

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-xl relative w-50">
        <button @click="closeModal" type="button" class="btn-close absolute top-5 right-3 text-gray-500 hover:text-gray-700"></button>
        <h2 class="text-xl font-bold mb-4">{{ formatDay(selectedDay.date) }}</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>AM</th>
              <th>PM</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="member in selectedMembers" :key="member">
              <td>{{ member }}</td>
              <td>{{ getStatusText(selectedDay, member, 'AM') }}</td>
              <td>{{ getStatusText(selectedDay, member, 'PM') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ChevronLeftIcon, ChevronRightIcon, CalendarIcon } from 'lucide-vue-next'
import axios from 'axios'

const views = ['Daily', 'Weekly', 'Monthly']
const currentView = ref('Weekly')
const currentDate = ref(new Date())
const formattedDateForInput = ref(currentDate.value.toISOString().slice(0, 10))

const statusColors = {
  'Work from Office': 'bg-blue-200',
  'Work from Home': 'bg-green-200',
  'On Leave': 'bg-gray-400'
}

const teamMembers = ref([])
const selectedMembers = ref([])
const isDropdownOpen = ref(false)
const schedule = ref([])

onMounted(async () => {
  try {
    const employee_obj = JSON.parse(sessionStorage.getItem("employee_obj"));
    console.log(employee_obj);
    const user_dept = employee_obj.Dept;
    const user_role = employee_obj.Role;

    const response = await axios.get('http://127.0.0.1:5000/wfh_request/deptSchedule', {
      headers: {
        'Dept': user_dept,
        'Role': user_role
      }
    });    
    schedule.value = response.data
    console.log(schedule.value)

    teamMembers.value = Object.keys(schedule.value);
    console.log('Team Members:', teamMembers.value);

    selectedMembers.value = teamMembers.value.slice(0, 1);
    console.log('Selected Members:', selectedMembers.value);
  } catch (error) {
    console.error('Error fetching schedule data:', error)
  }
})

const visibleDays = computed(() => {
  const days = [];
  let start = new Date(currentDate.value);
  let end = new Date(currentDate.value);

  if (currentView.value === 'Daily') {
    end.setDate(start.getDate() + 1);
  } else if (currentView.value === 'Weekly') {
    start.setDate(start.getDate() - start.getDay());
    end = new Date(start);
    end.setDate(start.getDate() + 7);
  }

  for (let d = new Date(start); d < end; d.setDate(d.getDate() + 1)) {
    const dateString = d.toISOString().split('T')[0];

    const dayStatus = selectedMembers.value.reduce((acc, member) => {
      const entries = schedule.value[member]?.filter(entry => 
        entry.Date.startsWith(dateString) && entry.Status === 'Approved'
      ) || [];

      // Default status assignment
      acc[member] = { AM: 'Work from Office', PM: 'Work from Office' };

      entries.forEach(entry => {
        if (entry.Duration === 'FD') {
          acc[member].AM = entry.Work_Arrangement; // Assign AM status
          acc[member].PM = entry.Work_Arrangement; // Assign PM status
        } else {
          acc[member][entry.Duration] = entry.Work_Arrangement; // Assign status based on duration
        }
      });

      return acc;
    }, {});

    days.push({
      date: new Date(d),
      status: dayStatus,
    });
  }

  return days;
});

const monthlyCalendar = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);

  const days = [];
  const startPadding = firstDay.getDay();
  const endPadding = 6 - lastDay.getDay();

  // Add padding days from previous month
  for (let i = startPadding - 1; i >= 0; i--) {
    const d = new Date(Date.UTC(year, month, -i));
    days.push({
      date: d,
      isCurrentMonth: false,
      status: {},
    });
  }

  // Current month days
  for (let d = 1; d <= lastDay.getDate(); d++) {
    const date = new Date(Date.UTC(year, month, d));
    const dateString = date.toISOString().split('T')[0];
    days.push({
      date,
      isCurrentMonth: true,
      status: selectedMembers.value.reduce((acc, member) => {
        const entries = schedule.value[member]?.filter(entry => entry.Date.startsWith(dateString) && entry.Status === 'Approved') || [];
        acc[member] = { AM: 'Work from Office', PM: 'Work from Office' };

        entries.forEach(entry => {
          if (entry.Duration === 'FD') {
            acc[member].AM = entry.Work_Arrangement; // Assign AM status
            acc[member].PM = entry.Work_Arrangement; // Assign PM status
          } else {
            acc[member][entry.Duration] = entry.Work_Arrangement; // Assign status based on duration
          }
        });

        return acc;
      }, {}),
    });
  }

  // Padding from next month
  for (let i = 1; i <= endPadding; i++) {
    const d = new Date(Date.UTC(year, month + 1, i));
    days.push({
      date: d,
      isCurrentMonth: false,
      status: {},
    });
  }

  return days;
});

const onDateChange = (e) => {
  const newDate = new Date(e.target.value)
  currentDate.value = newDate
}

const formattedDate = computed(() => {
  const options = { year: 'numeric', month: 'long' }

  if (currentView.value === 'Daily') {
    options.day = 'numeric'
    return currentDate.value.toLocaleDateString('en-US', options)
  }

  if (currentView.value === 'Weekly') {
    const startOfWeek = new Date(currentDate.value)
    startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay())  // Calculate startOfWeek first

    const endOfWeek = new Date(startOfWeek)  // Create endOfWeek after startOfWeek is finalized
    endOfWeek.setDate(startOfWeek.getDate() + 6)  // Set endOfWeek correctly
    
    return `${startOfWeek.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })} - ${endOfWeek.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })}`
  }

  return currentDate.value.toLocaleDateString('en-US', options)
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
  const status = day.status[member]?.[period];
  return statusColors[status] || 'bg-blue-100';
};

const getStatusText = (day, member, period) => {
  return day.status[member]?.[period] || 'Work from Office';
};

const getDayBackgroundColor = (day) => {
  if (!day.isCurrentMonth) return 'bg-blue-100'

  const statuses = Object.values(day.status).flatMap(s => [s.AM, s.PM])
  const counts = statuses.reduce((acc, status) => {
    acc[status] = (acc[status] || 0) + 1
    return acc
  }, {})
  
  const sortedCounts = Object.entries(counts).sort((a, b) => b[1] - a[1])
  if (sortedCounts.length > 1 && sortedCounts[0][1] === sortedCounts[1][1]) {
    return 'bg-white' // If tied, return white background
  }

  const majorityStatus = sortedCounts[0][0]
  
  switch (majorityStatus) {
    case 'Work from Office': return 'bg-blue-100'
    case 'Work from Home': return 'bg-green-100'
    case 'On Leave': return 'bg-gray-200'
    default: return 'bg-white'
  }
}

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const showModal = ref(false)
const selectedDay = ref(null)

const openModal = (day) => {
  selectedDay.value = day
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}
</script>