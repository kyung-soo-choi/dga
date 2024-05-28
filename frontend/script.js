const endpoint = 'http://localhost:8000/api'
function addSchedule() {
    const title = document.getElementById('schedule-title').value;
    const description = document.getElementById('schedule-description').value;
    const startDate = document.getElementById('schedule-start-date').value;
    const endDate = document.getElementById('schedule-end-date').value;

    fetch(`${endpoint}/schedules/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            description: description,
            start_date: startDate,
            end_date: endDate
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('schedule-title').value = '';
        document.getElementById('schedule-description').value = '';
        document.getElementById('schedule-start-date').value = '';
        document.getElementById('schedule-end-date').value = '';
        loadSchedules();
        loadCalendar();
    });
}
function showModal(todo) {
    document.getElementById('modal-todo-id').value = todo.id;
    document.getElementById('modal-todo-title').value = todo.title;
    document.getElementById('modal-todo-description').value = todo.description;
    document.getElementById('modal-todo-date').value = todo.date;
    document.getElementById('modal-todo-completed').checked = todo.completed;
    $('#todoModal').modal('show');
}
function showScheduleModal(schedule) {
    document.getElementById('modal-schedule-id').value = schedule.id || '';
    document.getElementById('modal-schedule-title').value = schedule.title || '';
    document.getElementById('modal-schedule-description').value = schedule.description || '';
    document.getElementById('modal-schedule-start-date').value = schedule.start_date || '';
    document.getElementById('modal-schedule-end-date').value = schedule.end_date || '';
    $('#scheduleModal').modal('show');
}
function loadCalendar() {
    const calendarEl = document.getElementById('calendar-data');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        height: 'auto',
        contentHeight: 'auto',
        events: fetchCalendarEvents,
        eventClick: function(info) {
            const event = info.event;
            if (event.extendedProps.type === 'todo') {
                showModal({
                    id: event.id,
                    title: event.title,
                    description: event.extendedProps.description,
                    date: event.startStr,
                    completed: event.extendedProps.completed
                });
            } else if (event.extendedProps.type === 'schedule') {
                showScheduleModal({
                    id: event.id,
                    title: event.title,
                    description: event.extendedProps.description,
                    start_date: event.startStr,
                    end_date: new Date(new Date(event.endStr).getTime() - 24 * 60 * 60 * 1000).toISOString().split('T')[0] // Subtract a day for display
                });
            }
        },
        eventContent: function(arg) {
            let italicEl = document.createElement('span');
            italicEl.innerHTML = arg.event.title;
            italicEl.style.cursor = 'pointer';
            if (arg.event.extendedProps.type === 'todo') {
                italicEl.addEventListener('click', function() {
                    showModal({
                        id: arg.event.id,
                        title: arg.event.title,
                        description: arg.event.extendedProps.description,
                        date: arg.event.startStr,
                        completed: arg.event.extendedProps.completed
                    });
                });
                if (arg.event.extendedProps.completed) {
                    italicEl.style.textDecoration = 'line-through';
                }
            } else if (arg.event.extendedProps.type === 'schedule') {
                italicEl.addEventListener('click', function() {
                    showScheduleModal({
                        id: arg.event.id,
                        title: arg.event.title,
                        description: arg.event.extendedProps.description,
                        start_date: arg.event.startStr,
                        end_date: new Date(new Date(arg.event.endStr).getTime() - 24 * 60 * 60 * 1000).toISOString().split('T')[0] // Subtract a day for display
                    });
                });
            }
            let arrayOfDomNodes = [italicEl];
            return { domNodes: arrayOfDomNodes };
        },
    });
    calendar.render();
}
function loadSchedules() {
    fetch(`${endpoint}/schedules/`)
        .then(response => response.json())
        .then(data => {
            const scheduleData = document.getElementById('schedule-data');
            scheduleData.innerHTML = '';

            data.forEach(schedule => {
                const scheduleItem = document.createElement('div');
                scheduleItem.classList.add('col-md-4');
                scheduleItem.innerHTML = `
                    <div class="card mb-4">
                        <div class="card-body">
                            <h5 class="card-title">${schedule.title}</h5>
                            <p class="card-text">${schedule.description}</p>
                            <p class="card-text">Start: ${schedule.start_date}</p>
                            <p class="card-text">End: ${schedule.end_date}</p>
                        </div>
                    </div>
                `;
                scheduleData.appendChild(scheduleItem);
            });
        })
        .catch(error => {
            console.error('Error loading schedules:', error);
        });
}
function fetchCalendarEvents(info, successCallback, failureCallback) {
    let events = [];

    fetch(`${endpoint}/todos/`)
        .then(response => response.json())
        .then(data => {
            const todoEvents = data.map(todo => ({
                id: todo.id,
                title: todo.title,
                start: todo.date,
                description: todo.description,
                completed: todo.completed,
                type: 'todo'
            }));
            events = events.concat(todoEvents);
            return fetch(`${endpoint}/schedules/`);
        })
        .then(response => response.json())
        .then(data => {
            const scheduleEvents = data.map(schedule => ({
                id: schedule.id,
                title: schedule.title,
                start: schedule.start_date,
                end: new Date(new Date(schedule.end_date).getTime() + 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                description: schedule.description,
                classNames: ['schedule-event'],
                type: 'schedule'
            }));
            events = events.concat(scheduleEvents);
            successCallback(events);
        })
        .catch(error => {
            console.error('Error fetching events:', error);
            failureCallback(error);
        });
}
function loadWeathers(){
    console.log('weathers loaded')
    const style = document.createElement('style');
style.textContent = `
  .weather-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .weather-info {
    flex: 1;
  }
  .weather-icon-container {
    flex: 0 0 auto;
  }
  .weather-icon {
    width: 50px;
    height: 50px;
  }
  /* 기본 레이아웃: 수직 배열 */
  .weather-column {
    display: flex;
    flex-direction: column;
  }
  /* 가로 길이가 1300px 이상일 때: 2열 배열 */
  @media (min-width: 1300px) {
    #weather-data {
      display: flex;
      flex-wrap: wrap;
    }
    .weather-day {
      flex: 1 1 50%; /* 반으로 나눠 배치 */
      box-sizing: border-box; /* 박스 크기 계산 포함 */
      padding: 10px; /* 간격 추가 */
    }
  }
`;
document.head.appendChild(style);


// Fetch weather data
  fetch(`${endpoint}/weather`)
    .then(response => response.json())
    .then(data => {
      const weatherDataElement = document.getElementById('weather-data');
      weatherDataElement.innerHTML = '';

      const today = new Date().toISOString().split('T')[0];
      const todayData = data.find(day => day.date === today);
      const otherData = data.filter(day => day.date !== today).sort((a, b) => new Date(a.date) - new Date(b.date));

      if (todayData) {
        const todayElement = document.createElement('div');
        todayElement.classList.add('weather-day', 'mb-3', 'weather-column');
        todayElement.innerHTML = `
          <div class="weather-container">
            <div class="weather-info">
              <h4>Today (${todayData.date})</h4>
              <p>Max Temp: ${parseFloat(todayData.max_temp - 273.15).toFixed(2)}°C</p>
              <p>Min Temp: ${parseFloat(todayData.min_temp - 273.15).toFixed(2)}°C</p>
            </div>
            <div class="weather-icon-container">
              <img src="http://openweathermap.org/img/wn/${todayData.icon}.png" alt="${todayData.icon}" class="weather-icon">
            </div>
          </div>
        `;
        weatherDataElement.appendChild(todayElement);
      }

      otherData.forEach(day => {
        const dayElement = document.createElement('div');
        dayElement.classList.add('weather-day', 'mb-3', 'weather-column');
        dayElement.innerHTML = `
          <div class="weather-container">
            <div class="weather-info">
              <h4>${day.weekday} (${day.date})</h4>
              <p>Max Temp: ${parseFloat(day.max_temp - 273.15).toFixed(2)}°C</p>
              <p>Min Temp: ${parseFloat(day.min_temp - 273.15).toFixed(2)}°C</p>
            </div>
            <div class="weather-icon-container">
              <img src="http://openweathermap.org/img/wn/${day.icon}.png" alt="${day.icon}" class="weather-icon">
            </div>
          </div>
        `;
        weatherDataElement.appendChild(dayElement);
      });
    })
    .catch(error => {
      document.getElementById('weather-data').innerHTML = 'Failed to load weather data';
      console.error('Error fetching weather data:', error);
    });
}
function loadTodos() {
    fetch(`${endpoint}/todos/`)
        .then(response => response.json())
        .then(data => {
            const todoData = document.getElementById('todo-data');
            todoData.innerHTML = '';

            const groupedByDate = data.reduce((acc, todo) => {
                const date = todo.date;
                if (!acc[date]) acc[date] = [];
                acc[date].push(todo);
                return acc;
            }, {});

            Object.keys(groupedByDate).forEach(date => {
                // const dateHeader = document.createElement('h4');
                // dateHeader.textContent = date;
                // dateHeader.classList.add('w-100'); // Make sure the date header takes full width
                // todoData.appendChild(dateHeader);

                groupedByDate[date].forEach(todo => {
                    if (!todo.completed) { // Show only non-completed todos
                        const todoItem = document.createElement('div');
                        todoItem.classList.add('col-md-4');
                        todoItem.innerHTML = `
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h5 class="card-title">${todo.date}</h5>
                                    <h5 class="card-title">${todo.title}</h5>
                                    <p class="card-text">${todo.description}</p>
                                    <button class="btn btn-success mt-2" onclick="toggleCompleted(${todo.id})">Complete</button>
                                    <button class="btn btn-danger mt-2" onclick="deleteTodo(${todo.id})">Delete</button>
                                    <button class="btn btn-secondary mt-2" onclick="editTodo(${todo.id})">Edit</button>
                                </div>
                            </div>
                        `;
                        todoData.appendChild(todoItem);
                    }
                });
            });
        });
}
function addTodo() {
    const title = document.getElementById('todo-title').value;
    const description = document.getElementById('todo-description').value;
    const date = document.getElementById('todo-date').value;

    fetch(`${endpoint}/todos/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            description: description,
            date: date,
            completed: false
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('todo-title').value = '';
        document.getElementById('todo-description').value = '';
        document.getElementById('todo-date').value = '';
        loadTodos();
        loadCalendar()
    });
}
function deleteTodo(id) {
    fetch(`${endpoint}/todos/${id}/`, {
        method: 'DELETE'
    })
    .then(() => {
        loadTodos();
        loadCalendar()
    });
}
function editTodo(id) {
    const title = prompt('Enter new title');
    const description = prompt('Enter new description');

    // Fetch the current todo to get the completed status
    fetch(`${endpoint}/todos/${id}/`)
        .then(response => response.json())
        .then(todo => {
            fetch(`${endpoint}/todos/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    date: todo.date,
                    completed: todo.completed // Keep the current completed status
                })
            })
            .then(response => response.json())
            .then(() => {
                loadTodos();
                loadCalendar()
            });
        });
}
function toggleCompleted(id) {
    fetch(`${endpoint}/todos/${id}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            completed: true
        })
    })
    .then(response => response.json())
    .then(() => {
        loadTodos();
        loadCalendar()
    });
}
document.addEventListener("DOMContentLoaded", function() {
    loadWeathers()
    loadTodos()
    loadCalendar()
    loadSchedules()

    const form = document.getElementById('todo-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        addTodo();
    });
    const scheduleForm = document.getElementById('schedule-form');
    scheduleForm.addEventListener('submit', function(e) {
        e.preventDefault();
        addSchedule();
    });

});
document.getElementById('save-schedule').addEventListener('click', function() {
    const id = document.getElementById('modal-schedule-id').value;
    const title = document.getElementById('modal-schedule-title').value;
    const description = document.getElementById('modal-schedule-description').value;
    const start_date = document.getElementById('modal-schedule-start-date').value;
    const end_date = document.getElementById('modal-schedule-end-date').value;

    const method = id ? 'PUT' : 'POST';
    const url = id ? `${endpoint}/schedules/${id}/` : `${endpoint}/schedules/`;

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            description: description,
            start_date: start_date,
            end_date: end_date
        })
    })
    .then(response => response.json())
    .then(() => {
        $('#scheduleModal').modal('hide');
        loadCalendar();
    });
});
document.getElementById('save-todo').addEventListener('click', function() {
    const id = document.getElementById('modal-todo-id').value;
    const title = document.getElementById('modal-todo-title').value;
    const description = document.getElementById('modal-todo-description').value;
    const date = document.getElementById('modal-todo-date').value;
    const completed = document.getElementById('modal-todo-completed').checked;

    if (id) {
        // Update existing todo
        fetch(`${endpoint}/todos/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                description: description,
                date: date,
                completed: completed // or keep the original completed status
            })
        })
        .then(response => response.json())
        .then(() => {
            loadTodos();
            loadCalendar();
            $('#todoModal').modal('hide');
        });
    } else {
        // Create new todo
        addTodo();
    }
});
document.getElementById('delete-schedule').addEventListener('click', function() {
    const id = document.getElementById('modal-schedule-id').value;
    if (id) {
        fetch(`${endpoint}/schedules/${id}/`, {
            method: 'DELETE'
        })
        .then(() => {
            $('#scheduleModal').modal('hide');
            loadCalendar();
        });
    }
});
document.getElementById('delete-todo').addEventListener('click', function() {
    const id = document.getElementById('modal-todo-id').value;
    if (id) {
        deleteTodo(id);
        $('#todoModal').modal('hide');
    }
});

setInterval(loadWeathers, 3 * 60 * 60 * 1000);
