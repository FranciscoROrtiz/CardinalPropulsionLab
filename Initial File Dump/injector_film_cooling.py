def injector_film_cooling(mdot_fuel, film_cooling_percentage):
    film_cooling_info = {
        'mdot_fuel_comb': mdot_fuel * (1 - film_cooling_percentage),
        'mdot_fuel_film': mdot_fuel * film_cooling_percentage}

    return film_cooling_info

