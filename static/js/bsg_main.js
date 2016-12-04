/**
 * Created by Tom on 19-Oct-16.
 * Care for var selected_position
 */

var world = ( function() {

    var world, galaxy, system, selected_position, fullscreen_window_height;
    var map_scroll_toggle = true;
    var next_turn_data = {};

    function __init(World) {
        world = World;
        galaxy = world['galaxy'];
        console.log(galaxy);

        next_turn_data = {
            actions: [
                ['warp', {
                    'selected_position': [1, 1],
                    'fleet': world['fleet_handler']['fleets'][0]
                }]
            ]
        };
    }

    function __canvas_fill(canvas_id, tile_id) {
        var c = document.getElementById(canvas_id);
        var ctx = c.getContext("2d");
        var img = document.getElementById(tile_id);
        var pat = ctx.createPattern(img, "repeat");

        ctx.rect(0, 0, c.width, c.height);
        ctx.fillStyle = pat;
        ctx.fill();
    }

    function starmap_height(star_map) {
        fullscreen_window_height = $(window).height() - 248;
        if (fullscreen_window_height > 2016) {
            star_map.height(2016);
        } else {
            star_map.height(fullscreen_window_height);
        }
    }

    function __generate_stars(star_map) {
        for (var sys in galaxy['system_list']) {
            var system = galaxy['system_list'][sys];
            var local_position = [system['global_position'][0] - galaxy['current_position'][0], system['global_position'][1] - galaxy['current_position'][1]];
            system.local_position = local_position;

            if (local_position[0] >= -30 && local_position[0] <= 30 && local_position[1] >= -30 && local_position[1] <= 30) {
                var src = system['file'][0];
                src.split(' ').join('_');

                var el = $("<img>").attr({
                    src: src,
                    alt: "star",
                    class: "solar-system",
                    "data-toggle": "tooltip",
                    "data-container": "body",
                    title: "(" + system['local_position'][0] + ", " + system['local_position'][1] + ")",
                    id: "(" + system['global_position'][0] + ", " + system['global_position'][1] + ")",
                    'global-x': system['global_position'][0],
                    'global-y': system['global_position'][1]
                }).css({
                    position: 'absolute',
                    left: (system['local_position'][0] + 30) * 32 + 32,
                    top: (-system['local_position'][1] + 30) * 32 + 32
                });
                star_map.append(el);
            }
        }
    }

    function __reset_star_map_canvas(e, star_map) {
        setTimeout(function(){
            star_map.scrollLeft((star_map[0].scrollWidth - star_map[0].clientWidth) / 2);
            star_map.scrollTop((star_map[0].scrollHeight - star_map[0].clientHeight)/ 2);
        }, 1);
    }

    function generate_canvas_and_stars(canvas_id, tile_id, star_map) {
        __canvas_fill(canvas_id, tile_id);
        starmap_height(star_map);
        __generate_stars(star_map);
    }

    function nav_div_links_onclick(e, el, star_map) {
        if (map_scroll_toggle) {
            if ($(el).attr('id') === 'map-link')  {
                __reset_star_map_canvas(e, star_map);
                map_scroll_toggle = false;
            }
        }
    }

    function solar_system_onclick(e, el) {
        var global_position = [Number($(el).attr('global-x')), Number($(el).attr('global-y'))];
        console.log(global_position);
        for (var sys in galaxy['system_list']) {
            if (galaxy['system_list'][sys]['global_position'][0] === global_position[0] && galaxy['system_list'][sys]['global_position'][1] === global_position[1]) {
                system = galaxy['system_list'][sys];
                break;
            }
        }

        $('#system-name').text(system['name']);
        $('#system-global-position').text("("+ system['global_position'][0] +", "+ system['global_position'][1] +")");
        $('#system-local-position').text("("+ system['local_position'][0] +", "+ system['local_position'][1] +")");
        $('#system-star-type').text(system['type']);
        $('#system-warp-chance').text(Math.sqrt (Math.pow(system['local_position'][0], 2) + Math.pow(system['local_position'][1], 2) ));

        var planets_list_card = $('#planets-list-card');
        planets_list_card.slideUp();

        setTimeout( function() {
            planets_list_card.html('');
            for (var plan in system['bodies']) {
                var planet = system['bodies'][plan];
                var planet_name_joined = planet['name'].split(' ').join('_');
                planets_list_card.append(
                    '<div class="list-group list-group-flush">' +
                        '<div class="card-header background-white">' +
                            '<a class="collapsed" data-toggle="collapse" href="#' + planet_name_joined + '" aria-expanded="true" aria-controls="' + planet_name_joined + '">' + planet['name'] + '</a>' +
                        '</div>' +
                        '<div id="' + planet_name_joined + '" class="collapse">' +
                            '<div class="card-block" style="border-bottom: 1px solid rgba(0,0,0,.125);">' +
                                '<ul> <li>Name: ' + planet['name'] +
                                '</li><li>Type: ' + planet['type'] +
                                '</li><li>Orbit: ' + planet['orbit'] +
                            '</li></ul></div>' +
                        '</div>' +
                    '</div>'
                );
            }
            var scroll_to = planets_list_card.offset().top + planets_list_card.height();
            planets_list_card.slideDown();
            $('html, body').animate({
                scrollTop: scroll_to
            }, 1000);
        }, 500);
    }

    function set_destination(e) {
        selected_position = system['global_position'];
        $('#warp').removeClass('disabled').removeClass('text-muted btn-outline-secondary').addClass('text-white btn-primary');
        $('#warp-coords').text('Warp Coords: ' + selected_position[0] + ', ' + selected_position[1]).removeClass('text-muted').addClass('text-white');
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
            success: function(server_data){
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

    return {
        init: __init,
        generate_canvas_and_stars: generate_canvas_and_stars,
        nav_div_links: nav_div_links_onclick,
        solar_system: solar_system_onclick,
        set_destination: set_destination,
        next_turn: next_turn_ajax,
        save_game_ajax: save_game_ajax,
        load_game_ajax: load_game_ajax,
        starmap_height: starmap_height
    };
})();