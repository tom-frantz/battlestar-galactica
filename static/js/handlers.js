/**
 * Created by Tom on 08-Dec-16.
 */

var map_scroll_toggle;

var handlers = ( function () {

    var local_systems_list;

    var galaxy_map = $('#galaxy-map');

    function __init(world) {
        console.log('Handlers initialized.');
        map_scroll_toggle = true;
        local_systems_list = world.get_local_systems_list();
        var tick = world.get_tick();
        $("#date-time").text(tick.getDate() + '/' + tick.getMonth() + '/' + tick.getFullYear() + " " + tick.getHours() + ":00")
    }

    function __draw_tiled_canvas(target_canvas_el, target_tile_el) {
        // Fills a canvas with a desired image. Tiles image.
        var c = target_canvas_el;
        var ctx = c.getContext("2d");
        var pat = ctx.createPattern(target_tile_el, "repeat");

        ctx.rect(0, 0, c.width, c.height);
        ctx.fillStyle = pat;
        ctx.fill();
    }

    function __set_galaxy_map_height() {
        // Sets the galaxy map height to the remainder of the height.
        var window_height = $(window).height() - 313;
        if (window_height >= 2016) {
            galaxy_map.height(2016);
        } else {
            galaxy_map.height(window_height);
        }
    }

    function __generate_stars(solar_systems_list) {
        // Only pass in solar systems within the local limits. [-30, -30] to [30, 30]
        console.log('Starting Star Generation.');
        for (var solar_system in solar_systems_list) {
            var system = solar_systems_list[solar_system];
            var src = system['file'];
            src = src.split(' ').join('_');

            var el = $("<img>", {
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

            galaxy_map.append(el);
        }
        console.log('Completed Star Generation.');
    }

    function __generate_fleet_cards(player_world) {
        console.log('Starting fleet card generation');
        var fleet_navs = $('#fleet_navigation_tabs');
        var fleet_content = $('#fleet_content_tabs');

        for (var fleet in player_world['fleet_handler']['fleets']) {
            var current_fleet = player_world['fleet_handler']['fleets'][fleet];
            console.log('current fleet :');
            console.log(current_fleet);
            var current_fleet_id = current_fleet['fleet_id'].split(' ').join('_');
            var nav_div = $('<li class="nav-item"></li>').append(
                '<a class="nav-link" data-toggle="tab" href="#' + current_fleet_id + '" role="tab">' + current_fleet['fleet_id'] + '</a>'
            );
            fleet_navs.append(nav_div);

            var tab_content_master = $('<div class="tab-pane fade" id="' + current_fleet_id + '"></div>');
            tab_content_master.append('<div class="col-md-12"></div>');
            var card_target = $('<div id="fleets' + current_fleet_id + '-list-card" class="card">');
            tab_content_master.append(card_target);

            for (var ship in current_fleet['ships']) {
                console.log('Current Ship: ');
                var current_ship = current_fleet['ships'][ship];
                console.log(current_ship);
                var current_ship_id = current_ship['id'];
                var ship_card = $('<div class="list-group list-group-flush"></div>');
                ship_card.append('<div class="card-header background-white"><a class="collapsed" data-toggle="collapse" href="#ship_' + current_ship_id + '">' + current_ship["name"] + '</a></div>');
                // TODO Add content per ship for stats and the likes.
                ship_card.append('<div id="ship_' + current_ship["id"] + '" class="collapse"><div class="card-block" style="border-bottom: 1px solid rgba(0,0,0,.125);">content</div></div>');
                console.log(ship_card);
                card_target.append(ship_card);
            }

            fleet_content.append(tab_content_master)
        }
    }

    function __center_scroll_galaxy_map() {
        // Scrolls to the center of the galaxy_map for view of current location.
        var scroll_to_hor = ( (2016 - galaxy_map.width()) / 2 );
        var scroll_to_ver = ( (2016 - galaxy_map.height()) / 2 );
        galaxy_map.animate({ scrollTop: scroll_to_ver, scrollLeft:scroll_to_hor})
    }

    function generate_html(player_world) {
        // Creates canvas and stars for the navigation menu
        __draw_tiled_canvas($('#star-canvas')[0], $('#star_tile')[0]);
        __set_galaxy_map_height(galaxy_map);
        __generate_stars(local_systems_list);
        __generate_fleet_cards(player_world);
    }

    function resize_window() {
        __set_galaxy_map_height(galaxy_map);
        var sidebar_height = $(document).height() - 54;
        $('#sidebar').height(sidebar_height);
    }

    function nav_click(trigger) {
        if (map_scroll_toggle) {
            if ($(trigger).attr('id') === 'map_link')  {
                setTimeout(__center_scroll_galaxy_map(galaxy_map), 400);
                map_scroll_toggle = false;
            }
        }
    }

    function star_click(el, world) {
        // NEEDS FIXING. Need to apply the local system list here.
        var global_position = [Number($(el).attr('global-x')), Number($(el).attr('global-y'))];
        for (var sys in local_systems_list) {
            if (local_systems_list[sys]['global_position'][0] === global_position[0] && local_systems_list[sys]['global_position'][1] === global_position[1]) {
                world.put_selected_system(local_systems_list[sys]);
                break;
            }
        }

        console.log(world.get_selected_system());
        var selected_system = world.get_selected_system();

        var planets_list_card = $('#planets-list-card');
        var solar_system_details = $("#map-galaxy-side-bar");

        planets_list_card.fadeOut();
        solar_system_details.fadeOut();

        setTimeout( function() {
            $('#system-name').text(selected_system.name);
            $('#system-global-position').text("("+ selected_system.global_position[0] +", "+ selected_system.global_position[1] +")");
            $('#system-local-position').text("("+ selected_system['local_position'][0] +", "+ selected_system['local_position'][1] +")");
            $('#system-star-type').text(selected_system['type']);
            $('#system-warp-chance').text(Math.sqrt (Math.pow(selected_system['local_position'][0], 2) + Math.pow(selected_system['local_position'][1], 2) ));

            planets_list_card.html('');
            for (var plan in selected_system['bodies']) {
                var planet = selected_system['bodies'][plan];
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
            planets_list_card.fadeIn(400);
            solar_system_details.fadeIn(400);
        }, 500);
    }

    function set_destination_click(world) {
        // Needs fixing for adjustment into the world's Selected_position variable
        var selected_position = world.get_selected_system()['global_position'];
        $('#warp').removeClass('disabled').removeClass('text-muted btn-outline-secondary').addClass('text-white btn-primary');
        $('#warp-coords').text('Warp Coords: ' + selected_position[0] + ', ' + selected_position[1]).removeClass('text-muted').addClass('text-white');
    }

    function saves_menu_link_click(trigger) {
        // Launches the save game modal. Dependent on what click it is
        if ($(trigger).attr('id') === 'save_game') {
            $("#saves_menu_button").text('Save Game').attr({'btn_type': 'save_game'});
            $('#save_name_text_bar').removeAttr('disabled');
        }
        else if ($(trigger).attr('id') === 'load_game') {
            $("#saves_menu_button").text('Load Game').attr({'btn_type': 'load_game'});
            $("#save_name_text_bar").attr({'disabled': ''});
        }
    }

    function saves_card_click(trigger) {
        $('#save_name_text_bar').val($(trigger).attr('id'));
        $('.card.card-block.card-save').removeClass('card-outline-primary');
        $(trigger).addClass('card-outline-primary');
    }

    function saves_button_click(e, trigger) {
        if ($(trigger).attr('btn_type') === 'save_game') {
            world.save_game_ajax(e, trigger, $('#save_name_text_bar').val());
        }
        else if ($(trigger).attr('btn_type') === 'load_game') {
            world.load_game_ajax(e, trigger, $('#save_name_text_bar').val());
        }
    }

    function toggle_sidebar_click(e) {
        e.preventDefault();
        $('#content-wrapper').toggleClass('toggled');
    }

    function re_center_map_content(galaxy_map) {
        __center_scroll_galaxy_map(galaxy_map)
    }

    function pause_button(trigger, world) {
        trigger = $(trigger);
        if (trigger.text() === "Pause" ) {
            trigger.text("Play");
            world.pause_game();
        } else if (trigger.text() === "Play") {
            trigger.text("Pause");
            world.play_game();
        }
    }

    return {
        init: __init,
        generate_html: generate_html,
        resize_window: resize_window,
        nav_click: nav_click,
        star_click: star_click,
        set_destination_click: set_destination_click,
        saves_menu_link_click: saves_menu_link_click,
        saves_card_click: saves_card_click,
        saves_button_click: saves_button_click,
        toggle_sidebar_click: toggle_sidebar_click,
        re_center_map_content: re_center_map_content,
        pause_button: pause_button
    }
})();