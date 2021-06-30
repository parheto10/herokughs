
!function($) {
    "use strict";

    var CalendarApp = function() {
        this.$body = $("body")
        this.$calendar = $('#calendar'),
        this.$event = ('#calendar-events div.calendar-events'),
        this.$categoryForm = $('#add_new_event form'),
        this.$extEvents = $('#calendar-events'),
        this.$modal = $('#my_event'),
        this.$saveCategoryBtn = $('.save-category'),
        this.$calendarObj = null
    };


    /* on drop */
    CalendarApp.prototype.onDrop = function (eventObj, date) { 
        var $this = this;
            // retrieve the dropped element's stored Event Object
            var originalEventObject = eventObj.data('eventObject');
            var $categoryClass = eventObj.attr('data-class');
            // we need to copy it, so that multiple events don't have a reference to the same object
            var copiedEventObject = $.extend({}, originalEventObject);
            // assign it the date that was reported
            copiedEventObject.start = date;
            if ($categoryClass)
                copiedEventObject['className'] = [$categoryClass];
            // render the event on the calendar
            $this.$calendar.fullCalendar('renderEvent', copiedEventObject, true);
            // is the "remove after drop" checkbox checked?
            if ($('#drop-remove').is(':checked')) {
                // if so, remove the element from the "Draggable Events" list
                eventObj.remove();
            }
    },
    /* on click on event */
    CalendarApp.prototype.onEventClick =  function (calEvent, jsEvent, view) {
        var $this = this;
            var form = $("<form></form>");
            form.append("<label>Change event name</label>");
            form.append("<div class='input-group'><input class='form-control' type=text value='" + calEvent.title + "' /><span class='input-group-append'><button type='submit' class='btn btn-success'><i class='fa fa-check'></i> Save</button></span></div>");
            $this.$modal.modal({
                backdrop: 'static'
            });
            $this.$modal.find('.delete-event').show().end().find('.save-event').hide().end().find('.modal-body').empty().prepend(form).end().find('.delete-event').unbind('click').click(function () {
                $this.$calendarObj.fullCalendar('removeEvents', function (ev) {
                    return (ev._id == calEvent._id);
                });
                $this.$modal.modal('hide');
            });
            $this.$modal.find('form').on('submit', function () {
                calEvent.title = form.find("input[type=text]").val();
                $this.$calendarObj.fullCalendar('updateEvent', calEvent);
                $this.$modal.modal('hide');
                return false;
            });
    },
    /* on select */
    CalendarApp.prototype.onSelect = function (start, end, allDay) {
        var $this = this;
            $this.$modal.modal({
                backdrop: 'static'
            });
            var form = $("<form method='post' enctype='multipart/form-data'></form>");
            form.append("<div class='event-inputs'></div>");
            form.find(".event-inputs")
                .append("<div class='form-group'><label class='control-label'>Date RDV :</label><input class='form-control datetimepicker' placeholder='Date RDV' type='text' name='date_rdv' id='id_date_rdv'/></div>")
                .append("<div class='form-group'><label class='control-label'>Poids :</label><input class='form-control' placeholder='Poids' type='number' step='0.1' name='poids' id='id_pods'/></div>")
                .append("<div class='form-group mb-0'><label class='check'>Symptômes : </label><checkbox name='symptomes'></checkbox></div>")
                .find("checkbox[name='symptomes']")
                .append("<div class='form-group mb-0'><label class='form-control' style='background-color: red' for='id_symptomes_0'><input class='form-check-input' id='id_symptomes_0' name='symptomes' title='' type='checkbox' value='6' /> AMAIGRISSEMENT</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control' for='id_symptomes_1'><input class='form-check-input' id='id_symptomes_1' name='symptomes' title='' type='checkbox' value='5' /> COURBATURES</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control' style='background-color: red' for='id_symptomes_2'><input class='form-check-input' id='id_symptomes_2' name='symptomes' title='' type='checkbox' value='2' /> CÉPHALÉE</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control danger' for='id_symptomes_3'><input class='form-check-input' id='id_symptomes_3' name='symptomes' title='' type='checkbox' value='9' /> DIARRHÉES</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control' for='id_symptomes_4'><input class='form-check-input' id='id_symptomes_4' name='symptomes' title='' type='checkbox' value='7' /> DIFFICULTÉS À RESPIRER</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control' for='id_symptomes_5'><input class='form-check-input' id='id_symptomes_5' name='symptomes' title='' type='checkbox' value='3' /> DOULEURS ABDOMINALES</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control' for='id_symptomes_6'><input class='form-check-input' id='id_symptomes_6' name='symptomes' title='' type='checkbox' value='4' /> DOULEURS DIFFUSES</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control' for='id_symptomes_7'><input class='form-check-input' id='id_symptomes_7' name='symptomes' title='' type='checkbox' value='1' /> FIÈVRE</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control' for='id_symptomes_8'><input class='form-check-input' id='id_symptomes_8' name='symptomes' title='' type='checkbox' value='10' /> SOIF</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control' for='id_symptomes_9'><input class='form-check-input' id='id_symptomes_9' name='symptomes' title='' type='checkbox' value='11' /> TENSION ÉLEVÉE</label></div>")
                .append("<div class='form-group mb-0'><label class='form-control' for='id_symptomes_10'><input class='form-check-input' id='id_symptomes_10' name='symptomes' title='' type='checkbox' value='12' /> VOMISSEMENTS</label></div>")
                .append("<div class='form-group'><label for='id_details'>Details</label><textarea name='details' cols='40' rows='10' class='form-control' placeholder='Details' title='Préciser les details de la dernieres Consultation SVP' id='id_details'></textarea><small class=\"form-text text-muted\">Préciser les details de la dernieres Consultation SVP</small></div>")
                // .append("<check value='bg-success'>Success</check>")
                // .append("<check value='bg-purple'>Purple</check>")
                // .append("<check value='bg-primary'>Primary</check>")
                // .append("<check value='bg-info'>Info</check>")
                // .append("<check value='bg-warning'>Warning</check></div></div>")
            ;
            $this.$modal.find('.delete-event').hide().end().find('.save-event').show().end().find('.modal-body').empty().prepend(form).end().find('.save-event').unbind('click').click(function () {
                form.submit();
            });
            $this.$modal.find('form').on('submit', function () {
                var title = form.find("input[name='title']").val();
                var beginning = form.find("input[name='beginning']").val();
                var ending = form.find("input[name='ending']").val();
                var categoryClass = form.find("select[name='category'] option:checked").val();
                if (title !== null && title.length != 0) {
                    $this.$calendarObj.fullCalendar('renderEvent', {
                        title: title,
                        start:start,
                        end: end,
                        allDay: false,
                        className: categoryClass
                    }, true);  
                    $this.$modal.modal('hide');
                }
                else{
                    alert('You have to give a title to your event');
                }
                return false;
                
            });
            $this.$calendarObj.fullCalendar('unselect');
    },
    CalendarApp.prototype.enableDrag = function() {
        //init events
        $(this.$event).each(function () {
            // it doesn't need to have a start or end
            var eventObject = {
                title: $.trim($(this).text()) // use the element's text as the event title
            };
            // store the Event Object in the DOM element so we can get to it later
            $(this).data('eventObject', eventObject);
            // make the event draggable using jQuery UI
            $(this).draggable({
                zIndex: 999,
                revert: true,      // will cause the event to go back to its
                revertDuration: 0  //  original position after the drag
            });
        });
    }
    /* Initializing */
    CalendarApp.prototype.init = function() {
        this.enableDrag();
        /*  Initialize the calendar  */
        var date = new Date();
        var d = date.getDate();
        var m = date.getMonth();
        var y = date.getFullYear();
        var form = '';
        var today = new Date($.now());
        var fr = {
            code: 'fr',
            week: {
              dow: 1, // Monday is the first day of the week.
              doy: 4, // The week that contains Jan 4th is the first week of the year.
            },
            buttonText: {
              prev: 'Précédent',
              next: 'Suivant',
              today: "Aujourd'hui",
              year: 'Année',
              month: 'Mois',
              week: 'Semaine',
              day: 'Jour',
              list: 'Planning',
            },
            weekText: 'Sem.',
            allDayText: 'Toute la journée',
            moreLinkText: 'en plus',
            noEventsText: 'Aucun événement à afficher',
          };

        // return fr;

        // var defaultEvents =  [{
        //         title: 'Event Name 4',
        //         start: new Date($.now() + 148000000),
        //         className: 'bg-purple'
        //     },
        //     {
        //         title: 'Test Event 1',
        //         start: today,
        //         end: today,
        //         className: 'bg-success'
        //     },
        //     {
        //         title: 'Test Event 2',
        //         start: new Date($.now() + 168000000),
        //         className: 'bg-info'
        //     },
        //     {
        //         title: 'Test Event 3',
        //         start: new Date($.now() + 338000000),
        //         className: 'bg-primary'
        //     }];

        var $this = this;
        $this.$calendarObj = $this.$calendar.fullCalendar({
            slotDuration: '00:15:00', /* If we want to split day time each 15minutes */
            minTime: '08:00:00',
            maxTime: '19:00:00',  
            defaultView: 'month',  
            handleWindowResize: true,   
             
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            // events: defaultEvents,
            editable: true,
            droppable: true, // this allows things to be dropped onto the calendar !!!
            eventLimit: true, // allow "more" link when too many events
            selectable: true,
            drop: function(date) { $this.onDrop($(this), date); },
            select: function (start, end, allDay) { $this.onSelect(start, end, allDay); },
            eventClick: function(calEvent, jsEvent, view) { $this.onEventClick(calEvent, jsEvent, view); }

        });

        //on new event
        this.$saveCategoryBtn.on('click', function(){
            var categoryName = $this.$categoryForm.find("input[name='category-name']").val();
            var categoryColor = $this.$categoryForm.find("select[name='category-color']").val();
            if (categoryName !== null && categoryName.length != 0) {
                $this.$extEvents.append('<div class="calendar-events" data-class="bg-' + categoryColor + '" style="position: relative;"><i class="fa fa-circle text-' + categoryColor + '"></i>' + categoryName + '</div>')
                $this.enableDrag();
            }

        });
    },

   //init CalendarApp
    $.CalendarApp = new CalendarApp, $.CalendarApp.Constructor = CalendarApp
    
}(window.jQuery),

//initializing CalendarApp
function($) {
    "use strict";
    $.CalendarApp.init()
}(window.jQuery);