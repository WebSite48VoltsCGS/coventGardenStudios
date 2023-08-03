document.addEventListener('DOMContentLoaded', function() {
  var newURL = window.location.protocol + "//" + window.location.host + "/salles/";
  var newURLAPI = window.location.protocol + "//" + window.location.host + "/api/all_booking_event/";

  $.ajax({
    url: newURL,
    method: 'GET', // HTTP method (GET, POST, etc.)
    dataType: 'json', // Expected data type of the response
    success: function(data) {
      console.log(newURL);
      console.log(newURLAPI);
      console.log("/salles/");
      console.log(data);
      var events_booking;
      
      $.ajax({
        url: newURLAPI,
        method: "GET",
        dataType: "json",
        success: function (datas) {
            events_booking = datas;
            console.log("/api/all_booking_event/");
            console.log(events_booking);
            for (let index = 1; index <= data.length; index++) {
              //const element = array[index];
              var name = "calendar"+index;
              var calendarEl = document.getElementById(name);
              console.log("event pour une ressource");
              var currentEvent = [];
              for (const event of events_booking) {
                if (event.resourceId == data[index-1].id) {
                  currentEvent.push(event);
                }
              }
              console.log(currentEvent);
              startCalendar(calendarEl, data[index-1], currentEvent);
            }
        },
        error: function (error) {
          alert("Error while fetching events");
        }
      });
     
    },
    error: function(error) {
      console.error(error);
    }
  });
  
  });
  
  function startCalendar(calendarEl, params, events_booking) {
  
    var calendar = new FullCalendar.Calendar(calendarEl, {
      timeZone: 'UTC',
      aspectRatio: 1.5,
      editable: false,
      selectable: true,
      locale: 'fr',
      slotDuration: '01:00',
      slotMinTime:"10:00",
      slotMaxTime:"23:59",
      initialView: 'timeGridWeek',
      firstDay: 1,  // Définit le lundi comme premier jour de la semaine
      allDaySlot: false,
      headerToolbar: {
        left: 'prev,next',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay' // user can switch between the two
      },
      events: events_booking,
      dateClick: function(info) {
        e.preventDefault();
        console.log(info);
        start = new Date(info.startStr).toISOString().replace('T', ' ').replace('Z', '').replace('.000', '');
        end = new Date(info.endStr).toISOString().replace('T', ' ').replace('Z', '').replace('.000', '');
        $('#salleName').val(params.title);
        $('#idSalle').val(params.id);
        $('#startDate').val(start);
        $('#endDate').val(end);
        $('#confirmation-modal').modal('show');

      },
      select: function(info) {
        start = new Date(info.startStr).toISOString().replace('T', ' ').replace('Z', '').replace('.000', '');
        end = new Date(info.endStr).toISOString().replace('T', ' ').replace('Z', '').replace('.000', '');
        $('#salleName').val(params.title);
        $('#idSalle').val(params.id);
        $('#startDate').val(start);
        $('#endDate').val(end);
        $('#confirmation-modal').modal('show');
        console.log(new Date(info.startStr));
      },
    });
    calendar.render();
  }