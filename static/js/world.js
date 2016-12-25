/**
 * Created by Tom on 19-Oct-16.
 * Care for var selected_position
 */

var world = (function () {
    // Need to make a function to grab all the systems in the local area. [-30, -30] to [30, 30]

    var player_world, selected_system, timer, tick;

    var event_queue = [];

    var update_events = {
        'resources': function (resources) {

        },
        'fleet_locations': function (fleet_location) {

        }
    };

    var local_systems_list = [];
    var map_scroll_toggle = true;

    function Event(event_id, ticks, tick_measure, params) {
        this.ticks_until_completion =  ticks;
        this.event_id = event_id; // The name of the method it will fire
        this.tick_measure = tick_measure; // 'monthly', 'daily', 'hourly' ...
        this.event_params = params;
    }

    function __init(World) {
        console.log('World initialized.');
        player_world = World;

        for (var solar_system in player_world['galaxy']['system_list']) {
            player_world['galaxy']['system_list'][solar_system].local_position = [
                // TODO Change from global position in world to primary fleet's location.
                player_world['galaxy']['system_list'][solar_system]['global_position'][0] - player_world['fleet_handler']['fleets'][0]['global_position'][0],
                player_world['galaxy']['system_list'][solar_system]['global_position'][1] - player_world['fleet_handler']['fleets'][0]['global_position'][1]
            ];

            var system = player_world['galaxy']['system_list'][solar_system];
            if (((-30 < system.local_position[0]) &&( system.local_position[0] < 30)) &&
                ((-30 < system.local_position[1]) && (system.local_position[1] < 30))) {
                local_systems_list.push(system)
            }
        }

        tick = new Date ('1942', '7', '23', '8', '0', '0', '0')
    }

    function __update_game_times() {
        $("#date-time").text(tick.getDate() + '/' + tick.getMonth() + '/' + tick.getFullYear() + " " + tick.getHours() + ":00")
    }

    function __game_loop() {
        // IN PROGRESS AJAX back the data that needs to be processed.
        $.ajax({
            type: 'POST',
            url: '/event_loop',
            data: JSON.stringify(event_queue),
            dataType: 'json',
            contentType: 'application/json',
            success: function (server_data) {
                // IN PROGRESS Process information and redisplay on the clientside.
                // Returns 'event_name' and 'params' for each update_event sent back from the server.

                // Sets the new tick
                tick = server_data['tick'];

                // Clears out the event queue for new data inputs
                event_queue = [];

                // Refreshes values from the server.
                for (var event in server_data) {
                    var current_event = server_data[event];
                    update_events[current_event['event_name']](current_event['params'])
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {alert('Error: Unable to load page: ' + thrownError);}
        });
        // IN PROGRESS Update the HTML page with relevant information (DO IN AJAX).
        __update_game_times();
    }
    
    function next_turn_ajax(e, el) {
        $.ajax({
            type: 'POST',
            url: '/next_turn',
            data: JSON.stringify({
                'next_turn_type': $(el).attr('id'),
                'selected_position': selected_position
            }),
            dataType: 'json',
            contentType: 'application/json',
            success: function (server_data) {
                if (server_data['success'] === true) {
                    location.reload();
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {alert('Error: Unable to load page: ' + thrownError);}
        });
    }

    function save_game_ajax(e, el, save_game_name) {
        $.ajax({
            type: 'POST',
            url: '/save_game',
            data: JSON.stringify({
                'save_name': save_game_name
            }),
            dataType: 'json',
            contentType: 'application/json',
            success: function (server_data) {
                alert('Game Updated.');
                console.log($('[id = "' + save_game_name + '"]'));
                $('[id = "' + save_game_name + '"] .modified_time').text('Last Modified: ' + server_data['time']);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert('Error: Unable to load page: ' + thrownError);
            }
        })
    }

    function load_game_ajax(e, el, load_game_name) {
        $.ajax({
            type: 'POST',
            url: '/load_game',
            data: JSON.stringify({
                'load_name': load_game_name
            }),
            dataType: 'json',
            contentType: 'application/json',
            success: function (server_data) {
                if (server_data['valid'] === true) {
                    alert('Load game successful.');
                    location.reload();
                }
                else {
                    alert('Load game unsuccessful.')
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert('Error: Unable to load page: ' + thrownError);
            }
        })
    }

    function play_game() {
        timer = setInterval(__game_loop, 1000);
    }

    function pause_game() {
        clearInterval(timer)
    }

    // TODO Get and put functions within one function per var.
    // E.G. A function to put and get the selected system.

    function get_player_world() {
        return player_world;
    }

    function get_local_systems_list() {
        return local_systems_list;
    }

    function get_selected_system() {
        return selected_system;
    }

    function put_selected_system(selected_sys) {
        selected_system = selected_sys;
    }

    function get_tick() {
        return tick
    }

    return {
        init: __init,
        next_turn: next_turn_ajax,
        save_game_ajax: save_game_ajax,
        load_game_ajax: load_game_ajax,
        play_game: play_game,
        pause_game: pause_game,

        // Functions to grab/put variables.
        player_world: get_player_world,
        get_local_systems_list: get_local_systems_list,
        get_selected_system: get_selected_system,
        put_selected_system: put_selected_system,
        get_tick: get_tick
    };
})();