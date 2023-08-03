document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var events;
  var newURL = window.location.protocol + "//" + window.location.host + "/all_events/";

  $.ajax({
    url: newURL,
    method: "GET",
    dataType: "json",
    success: function (datas) {
      events = datas;
      initializeCalendar();
    },
    error: function (error) {
      alert("Error while fetching events");
    }
  });

  function initializeCalendar() {
    var calendar = new FullCalendar.Calendar(calendarEl, {
      headerToolbar: {
        left: 'prev,next',
        center: 'title',
        right: '',
      },
      locale: 'fr',
      editable: false,
      firstDay: 1,
      slotMinTime: '10:00',
      slotMaxTime: '23:59',
      slotDuration: '01:00',
      allDaySlot: false,
      events: events,
    });

    calendar.render();
  }
});
