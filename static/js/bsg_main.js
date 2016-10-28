/**
 * Created by Tom on 19-Oct-16.
 * Care for var selected_position
 */

var world = ( function() {

    var world, galaxy, system, selected_position;

    function __init(World) {
        world = World;
        galaxy = World['galaxy'];
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

    function __starmap_height(star_map) {
        var window_height = $(window).height() - 180;
        if (window_height > 2016) {
            star_map.height(2016);
        } else {
            star_map.height(window_height);
        }
    }

    function __generate_stars(star_map) {
        for (var sys in galaxy['system_list']) {
            var local_position = [galaxy['system_list'][sys]['global_position'][0] - galaxy['current_position'][0], galaxy['system_list'][sys]['global_position'][1] - galaxy['current_position'][1]];
            galaxy['system_list'][sys].local_position = local_position

            if (local_position[0] >= -30 && local_position[0] <= 30 && local_position[1] >= -30 && local_position[1] <= 30) {
                var src = galaxy['system_list'][sys]['file'][0];
                src.split(' ').join('_');

                var el = $("<img>").attr({
                    src: src,
                    alt: "star",
                    class: "solar-system",
                    "data-toggle": "tooltip",
                    "data-container": "body",
                    title: "(" + local_position[0] + ", " + local_position[1] + ")",
                    id: "(" + galaxy['system_list'][sys]['global_position'][0] + ", " + galaxy['system_list'][sys]['global_position'][1] + ")",
                    'global-x': galaxy['system_list'][sys]['global_position'][0],
                    'global-y': galaxy['system_list'][sys]['global_position'][1]
                }).css({
                    position: 'absolute',
                    left: (local_position[0] + 30) * 32 + 32,
                    top: (-local_position[1] + 30) * 32 + 32
                });
                star_map.append(el);
            }
        }
    }

    function generate_canvas_and_stars(canvas_id, tile_id, star_map) {
        __canvas_fill(canvas_id, tile_id);
        __starmap_height(star_map);
        __generate_stars(star_map);
    }

    function nav_div_links_onclick(e, star_map) {
        setTimeout(function(){
            star_map.scrollLeft((star_map[0].scrollWidth - star_map[0].clientWidth) / 2);
            star_map.scrollTop((star_map[0].scrollHeight - star_map[0].clientHeight)/ 2);
        }, 1);
    }

    function solar_system_onclick(e, el) {
        var global_position = [Number($(el).attr('global-x')), Number($(el).attr('global-y'))];
        console.log(global_position);
        for (var sys in galaxy['system_list']) {
            if (galaxy['system_list'][sys]['global_position'][0] === global_position[0] && galaxy['system_list'][sys]['global_position'][1] === global_position[1]) {
                system = galaxy['system_list'][sys];
            }
        }
        $('#system-name').text(system['name']);
        $('#system-global-position').text("("+ system['global_position'][0] +", "+ system['global_position'][1] +")");
        $('#system-local-position').text("("+ system['local_position'][0] +", "+ system['local_position'][1] +")");
        $('#system-star-type').text(system['type']);
        $('#system-warp-chance').text(Math.sqrt (Math.pow(system['local_position'][0], 2) + Math.pow(system['local_position'][1], 2) ));
    }

    function set_destination(e) {
        selected_position = system['global_position'];
        $('#warp').attr({'disabled': false});
        $('#warp-coords').attr({'hidden': false}).text('Warp Coords: ' + selected_position);
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
                if (server_data['refresh'] === true) {
                    location.reload();
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert('Error: Unable to load page: ' + thrownError);
            }
        })
    }

    function run_event(e) {
        var options = $('#options').html('');
        if (current_path[0] === 'dialogs') {
            for (var option in event[current_path[0]][current_path[1]]['options']) {
                var el = $('<button></button>').attr({
                    type: 'button',
                    'class': 'btn btn-default btn-options',
                    'option-path': event[current_path[0]][current_path[1]]['options'][option]['path'],
                    'option-type': event[current_path[0]][current_path[1]]['options'][option]['type'],
                    'data-dismiss': 'modal'
                }).text(event[current_path[0]][current_path[1]]['options'][option]['text']);
                options.append(el);
            }
        }

        $('#modal-text').html("<p>" + event[current_path[0]][current_path[1]]['text'] + "</p>");

        if (current_path[0] === 'outcomes') {
            for (var outcome in event[current_path[0]][current_path[1]]['outcome']) {
                el = $('<p></p>').attr({
                    'class': event[current_path[0]][current_path[1]]['outcome'][outcome][1]
                }).text(event[current_path[0]][current_path[1]]['outcome'][outcome][0]);
                $('#modal-effects').append(el)
            }
            options.append('<button type="button" class="btn btn-default btn-event-finished" data-dismiss="modal">Close</button>')
        }
    }

    return {
        init: __init,
        generate_canvas_and_stars: generate_canvas_and_stars,
        nav_div_links: nav_div_links_onclick,
        solar_system: solar_system_onclick,
        set_destination: set_destination,
        next_turn: next_turn_ajax

    };
})();