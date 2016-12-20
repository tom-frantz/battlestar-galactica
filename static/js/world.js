/**
 * Created by Tom on 19-Oct-16.
 * Care for var selected_position
 */

var world = (function () {
    // Need to make a function to grab all the systems in the local area. [-30, -30] to [30, 30]

    var player_world, selected_system, timer;

    var local_systems_list = [];
    var map_scroll_toggle = true;
    var next_turn_data = {};

    function __init(World) {
        player_world = World;
        console.log('World: '); console.log(player_world);

        next_turn_data = {
            actions: [
                ['warp', {
                    'selected_position': [1, 1],
                    'fleet': player_world['fleet_handler']['fleets'][0]
                }]
            ]
        };

        for (var solar_system in player_world['galaxy']['system_list']) {
            player_world['galaxy']['system_list'][solar_system].local_position = [
                player_world['galaxy']['system_list'][solar_system]['global_position'][0] - player_world['galaxy']['current_position'][0],
                player_world['galaxy']['system_list'][solar_system]['global_position'][1] - player_world['galaxy']['current_position'][1]
            ];

            var system = player_world['galaxy']['system_list'][solar_system];
            if (((-30 < system.local_position[0]) &&( system.local_position[0] < 30)) &&
                ((-30 < system.local_position[1]) && (system.local_position[1] < 30))) {
                local_systems_list.push(system)
            }
        }
    }

    function __game_loop() {

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
            error: function (xhr, ajaxOptions, thrownError) {
                alert('Error: Unable to load page: ' + thrownError);
            }
        })
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

    // Get and put functions

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

    return {
        init: __init,
        next_turn: next_turn_ajax,
        save_game_ajax: save_game_ajax,
        load_game_ajax: load_game_ajax,
        play_game: play_game,
        pause_game: pause_game,

        // Functions to grab/put variables.
        player_world: get_player_world,
        local_systems_list: get_local_systems_list,
        get_selected_system: get_selected_system,
        put_selected_system: put_selected_system
    };
})();