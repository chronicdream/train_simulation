# -*- coding: utf-8 -*-
"""
DA2004 VT2023 - INDU: Trains

"""

import random   # for Train instancing and simulate_turn() method.


class Station:
    """
    Station objects represent train stations in a rail network.
    They have a name and a probability of delays occurring at them.
    """

    def __init__(self, name, delay_constant):
        """
        Constructor.

        Parameters
        ----------
        name : str
            Station name, for identification by various methods.
        delay_constant : float : 0 <= x < 1
            Probability of delays occurring at station.

        Returns
        -------
        None.
        """
        self.name = name
        self.delay_constant = delay_constant
        self.connections = []

    def verify_stations(filename):
        """
        Verifies that a file containing station data is formatted correctly.
        To pass, lines in the file must meet the requirements:
            1. contains exactly 2 columns, separated by a comma
            2. column 2 must be a number 0 <= x < 1.

        Parameters
        ----------
        filename : str
            Name of the file to be checked.

        Raises
        ------
        ValueError
            If file contains lines with bad data, such as an inappropriate
            number of columns or incorrect type of data.

        Returns
        -------
        bool
            If no issues are found in the file, returns True.
        """
        with open(filename, 'r') as data:
            for line in data.readlines():
                if len(line.strip('\n').split(',')) != 2:
                    raise ValueError
                else:
                    delay = float(line.strip('\n').split(',')[-1])
                    if delay < 0 or delay >= 1:
                        raise ValueError
        return True


    def format_stations(file_handle):
        """
        Reads data from a file handle and converts the contents into a list.

        Parameters
        ----------
        file_handle : file object handle
            Handle for the file to be parsed.

        Returns
        -------
        station_list : list
            tuple elements of the format:
                (name = str, delay constant = float)
        """
        station_list = []
        with file_handle as data:
            for line in data.readlines():
                line = line.upper().strip('\n').split(',')
                line_tuple = (line[0], float(line[-1]))
                # converts column 2 to avoid storing a decimal as str
                station_list.append(line_tuple)
        return station_list


    def prime_stations(filename):
        """
        Driver method for verify_stations and format_stations.
        Takes a file name, verifies it as a valid source of station data,
        and converts it into a list for later use.

        Parameters
        ----------
        filename : str
            Name of the file to be used.

        Raises
        ------
        ValueError
            If issues are detected by verify_stations.
        error
            If another exception is found, such as FileNotFound.

        Returns
        -------
        stations_list : list
            Output from format_stations.
        """
        try:
            stations_file = open(filename, 'r')
            if Station.verify_stations(filename) is True:
                stations_list = Station.format_stations(stations_file)
                stations_file.close()
                return stations_list
            else:
                raise ValueError
        except BaseException as error:
            raise error


    def verify_connections(filename):
        """
        Verifies that a file containing station data is formatted correctly.
        To pass, lines in the file must meet the requirements:
            1. contains exactly 4 columns, separated by a comma
            2. column 4 must be either "s" or "n" (not case sensitive).

        Parameters
        ----------
        filename : str
            Name of the file to be used.

        Raises
        ------
        ValueError
            If file contains lines with bad data, such as an inappropriate
            number of columns or incorrect type of data.

        Returns
        -------
        bool
            If no issues are found, returns True.
        """
        with open(filename, 'r') as data:
            for line in data.readlines():
                line = line.strip('\n').split(',')
                if len(line) != 4:
                    raise ValueError
                elif line[-1] not in ['N', 'n', 'S', 's']:
                    raise ValueError
                    # column 4 must represent North/South
        return True


    def format_connections(file_handle):
        """
        Reads data from a file handle and converts the contents into a list.

        Parameters
        ----------
        file_handle : file_handle : file object handle.
            Handle for the file to be parsed.

        Returns
        -------
        connections_list : list
            tuple elements of the format:
                (name, connection, line, direction), all elements = str
        """
        connections_list = []
        with file_handle as data:
            for line in data.readlines():
                line = line.upper().strip('\n').split(',')
                connections_list.append(tuple(line))
        return connections_list


    def prime_connections(filename):
        """
        Driver method for verify_connections and format_connections.
        Takes a file name, verifies it as a valid source of station data,
        and converts it into a list for later use.

        Parameters
        ----------
        filename : str
            Name of the file to be used.

        Raises
        ------
        ValueError
            If issues are detected by verify_connections.
        error
            If another exception is found, such as FileNotFound.

        Returns
        -------
        stations_list : list
            Typically output from format_connections.
        """
        try:
            if Station.verify_connections(filename) is True:
                connections_file = open(filename, 'r')
                connections_list = Station.format_connections(connections_file)
                connections_file.close()
                return connections_list
            else:
                raise ValueError
        except BaseException as error:
            raise error


    def build_catalog(station_list):
        """
        Generates a dictionary containing all Station class instances.

        Parameters
        ----------
        station_list : List
            Data source for dictionary comprehension.
            Typically output from prime_stations / format_stations.

        Returns
        -------
        catalog : dict
            Station names are used as keys. (=str)
            Values are Station class objects.
        """
        catalog = {station: Station(station, delay_constant)
                   for station, delay_constant in station_list}
        return catalog


    def map_connections(stations_list, connections_list):
        """
        Populates connections class attribute for objects in a Station dict.

        Parameters
        ----------
        stations_list : list
            List containing station information.
            Typically output from format_stations.
        connections_list : list
            List containing connections information.
            Typically output from format_connections.

        Returns
        -------
        catalog : dict
            Updated Station class dictionary. Same structure as input,
            but with connections attribute populated.
        """
        catalog = Station.build_catalog(stations_list)
        for element in connections_list:
            catalog[element[0]].connections.append(element[1:])
        for element in connections_list:
            if element[-1] == 'S':
                inverse = (element[0], element[2], 'N')
            else:
                inverse = (element[0], element[2], 'S')
            catalog[element[1]].connections.append(inverse)
            # inverse connections go from b -> a if a -> b exists
        return catalog


    def build_graph(station_catalog):
        """
        Generates a dictionary containing only Station names
        and connecting Station names. Used by breadth_first_pathfind method.

        Parameters
        ----------
        station_catalog : dict
            Dictionary of Station class objects.
            Typically output from build_catalog.

        Returns
        -------
        graph : dict
            Station names are used as keys. (=str)
            Values are lists of connecting Station names. (elements = str)
        """
        graph = {key: [] for key in station_catalog.keys()}
        for key, value in station_catalog.items():
            for entry in value.connections:
                graph[key].append(entry[0])
        return graph


    def breadth_first_pathfind(graph, start, goal):
        """
        Finds the shortest path between two stations.
        Uses "breadth first search" algorithm to find the shortest path.

        Connecting stations are visited in order of distance from the root.
        Connections at n+1 distance are then stored, and visited later if no
        path could be found at distance n.
        As search progresses, the path taken is traced. Stations which have
        already been searched will not be repeated. Search continues until
        target is found, or there are no more stations left to search.

        Parameters
        ----------
        graph : dict
            Dictionary containig Stations and their direct neighbours.
        start : str
            Root station from which to begin search.
        goal : str
            Destination to be found and shortest path to traced.

        Returns
        -------
        shortest_path : list
            If goal station is found, returns the path taken as a list.
        queue: list
            If goal station cannot be found, returns the queue (empty list).
        """
        explored = []
        # tracks stations that have already been searched
        queue = [[start]]
        while queue:
            search_path = queue.pop(0)
            station = search_path[-1]
            # unexplored stations are always at the end of queue elements
            if station not in explored:
                connections = graph[station]
                for neighbour in connections:
                    shortest_path = list(search_path)
                    shortest_path.append(neighbour)
                    # trace path taken
                    queue.append(shortest_path)
                    # add search candidate to the queue
                    if neighbour == goal:
                        return shortest_path
                explored.append(station)
        # if queue becomes empty, target could not be found
        return queue



class Train:
    """
    Train objects represent trains moving along tracks in a rail network.
    They have names, and contain information about their current location,
    which line they belong to, and their current course (north-/southbound).
    """

    def __init__(self, name, station, line, course):
        """
        Constructor.

        Parameters
        ----------
        name : str
            Train name, for identification by various methods.
        station : str
            Current station where train has stopped.
        line : str
            Line which the train belongs to. Can only move along this line.
        course : str ('N' or 'S')
            Current course, representing northbound or southbound direction.

        Returns
        -------
        None.

        """
        self.name = name
        self.station = station
        self.line = line
        self.course = course


    def build_catalog(station_catalog, train_count):
        """
        Generates a specified number of Train objects, based on input.
        Trains are randomly assigned a station, line, and course.
        Will only choose lines that are available at their assigned station.

        random module is used for attribute assignments.

        Parameters
        ----------
        station_catalog : dict
            Dictionary containing Station objects and their attributes.
            Attributes used here are name and connections.
        train_count : int
            Number of trains to be generated.

        Returns
        -------
        catalog : dict
            Returns a dictionary containing all train objects as values.
            Keys are generated as natural numbers and converted to str.

        """
        stations = list(station_catalog.keys())
        courses = ['N', 'S']
        catalog = {str(n + 1): Train(n + 1, random.choices(stations)[0],
                                   '', random.choices(courses)[0])
                   for n in range(train_count)}
        # line attribute is empty str, as it depends on assigned station
        for key in catalog:
            line_options = []
            for connection in station_catalog[catalog[key].station].connections:
                if connection[1] not in line_options:
                    line_options.append(connection[1])
            catalog[key].line = random.choice(line_options)
        # line attribute is now populated based on available connections
        return catalog


    def reverse(self):
        """
        Switches course direction for trains that have reached an end station.

        Returns
        -------
        course : str
            New course, opposite of previous.

        """
        if self.course == 'N':
            self.course = 'S'
        else:
            self.course = 'N'
        return self.course


    def move(self, station_catalog):
        """
        Moves trains by one time unit.
        Trains first check for connections matching line/course.
        If no match is found, reverses course.
        Finally, moves trains to the next station on their line.

        Parameters
        ----------
        sation_catalog : dict
            Dictionary containing Station objects and their attributes.

        Returns
        -------
        bool
            Returns True if movement was successful.
            Returns False if no match could be found in either direction
            (to identify issues like broken connections in rail network)

        """
        connections_data = [connection[1:] for connection
                            in station_catalog[self.station].connections]
        match = (self.line, self.course) in connections_data
        # if no match is found, train is at end station
        if match == False:
            self.reverse()
            # reverse course since train must be at end station
        for connection in station_catalog[self.station].connections:
            if self.line in connection and self.course in connection:
                self.station = connection[0]
                return True
        return False


    def simulate_turn(station_catalog, train_catalog):
        """
        Simulates railway network model, increments by 1 time unit (1 "turn").
        Trains first roll a delay check based on their current station.
        If check fails, trains stay where they are.
        If check passes, calls .move() method on trains.

        random module is used to roll for delays.

        Parameters
        ----------
        station_catalog : dict
            Dictionary containing Station objects and their attributes.
        train_catalog : dict
            Dictionary containing Train objects and their attributes.

        Returns
        -------
        train_catalog : dict
            Returns updated Train object dictionary.

        """
        for train in train_catalog.values():
            current_location = station_catalog[train.station]
            if float(current_location.delay_constant) > random.random():
                continue
            # roll for delay
            else:
                train.move(station_catalog)
        return train_catalog


    def lookup_info(self):
        """
        Collects train attributes into a string for printing.

        Returns
        -------
        output : str
            Train name, line, course, and station.

        """
        output = ''
        if self.course == 'N':
            output += 'Train ' + str(self.name) + ' on ' + self.line + ' line '
            output += 'Northbound is at station ' + self.station + '.\n'
            return output
        else:
            output += 'Train ' + str(self.name) + ' on ' + self.line + ' line '
            output += 'Southbound is at station ' + self.station + '.\n'
            return output


def submenu_2(train_catalog):
    """
    User menu used for lookup_info method.
    Validates user input as an existing Train key, and prints attributes.

    Parameters
    ----------
    train_catalog : dict
        Dictionary containing Train objects and their attributes.

    Returns
    -------
    None.
    Prints return string from lookup_info.

    """
    try:
        train = input('Choose a train [1 - ' +
                        str(len(train_catalog)) + ']:\n')
        print(Train.lookup_info(train_catalog[train]))
    except KeyError:
        print('Invalid input. Please enter an integer within the '
              'listed range.\n')


def submenu_3(station_catalog):
    """
    User menu for breath_first_pathfind method.
    Validates user input as existing nonequal Station keys.
    Calls breath_first_pathfind with user input parameters.
    Prints one of three responses based on the results:
        1. Destination can be reached within specified number of time units.
        2. Destination cannot be reached within specified number of time units.
        3. There is no railway between the point of origin and the destination.

    Parameters
    ----------
    station_catalog : dict
        Dictionary containing Station objects and their attributes.

    Raises
    ------
    KeyError
        If user selects invalid station name(s).
    UserWarning
        If user selects the same starting point and end point.
    ValueError
        If user inputs invalid data for time units.

    Returns
    -------
    None.

    """
    try:
        root = input('Select a starting point:\n').upper()
        goal = input('Select a destination:\n').upper()
        steps = int(input('Enter a number to check if destination is '
                          'reachable within that many time units:\n'))
        if root == goal:
            raise UserWarning()
        elif steps < 0:
            raise ValueError
        else:
            graph = Station.build_graph(station_catalog)
            path = Station.breadth_first_pathfind(graph, root, goal)
            if len(path) == 0:
                print('No route found between stations', root,
                      'and', goal + '.\n')
            elif len(path[1:]) > steps:
                # slice away first element in list, as it represents the root
                print('Station', goal, 'cannot be reached from', 'station',
                      root, 'within', str(steps), 'time units.\n')
            else:
                print('Station', goal, 'can be reached from', 'station',
                      root, 'within', str(steps), 'time units.\n')
    except KeyError:
        print('Invalid input. Starting point and destination must be '
              'valid stations. Please verify and try again.\n')
    except UserWarning:
        print('Invalid input. Starting point and destination '
              'must be different.\n')
    except ValueError:
        print('Invalid input. Number must be a positive integer.\n')


def simulation_menu(station_catalog, train_catalog):
    """
    Main menu for railway network model. User may choose to:
        1. Run simulation
        2. View train attributes
        3. Check if station B can be reached from station A within X time.
        4. Quit program.
    Menu loops until Quit is selected.

    Parameters
    ----------
    station_catalog : dict
        Dictionary containing Station objects and their attributes.
    train_catalog : dict
        Dictionary containing Train objects and their attributes.

    Returns
    -------
    None.
    Calls Train.simulate_turn, submenu_2, or submenu_3.

    """
    while True:
        choice = input('To run simulation, enter [1]\n'
                        'To access train information, enter [2]\n'
                        'To access route information, enter [3]\n'
                        'To exit, enter [Q]\n')
        if choice == '1':
            Train.simulate_turn(station_catalog, train_catalog)
            print('Simulation successfully incremented by 1 time unit.\n')
        elif choice == '2':
            submenu_2(train_catalog)
        elif choice == '3':
            submenu_3(station_catalog)
        elif choice in ['Q', 'q']:
            print('Shutting down. Have a nice day!')
            break
        else:
            print('Invalid input. Please try again.\n')


def main():
    """
    Main driver function for the program. Prompts user to provide
    files necessary to initialize model, and number of trains to create.
    Loops in stages until valid input is given.

    Returns
    -------
    None.
    Primes simulation by calling Station.prime_stations,
    Station.prime_connections, Station.map_connections, and
    Train.build_catalog, then proceeds to simulation_menu.

    """
    print('Welcome. To begin, please provide simulation parameters.\n')
    loop = 0
    while loop == 0:
        try:
            file_1 = input('Enter name of stations file:\n')
            stations_list = Station.prime_stations(file_1)
            loop = 1
        except FileNotFoundError:
            print('Cannot open', file_1 + '. Please try again.\n')
        except ValueError:
            print('File', file_1, 'is not formatted correctly or contains '
                  'unexpected values. Please check the file for errors '
                  'and try again, or choose a different file.\n')
    while loop == 1:
        try:
            file_2 = input('Enter name of connections file:\n')
            connections_list = Station.prime_connections(file_2)
            station_catalog = Station.map_connections(stations_list, connections_list)
            loop = 2
        except FileNotFoundError:
            print('Cannot open', file_2 + '. Please try again.\n')
        except (ValueError, KeyError):
            print('File', file_2, 'is not formatted correctly or contains '
                  ' unexpected values. Please check the file for errors '
                  'and try again, or choose a different file.\n')
    while loop == 2:
        try:
            train_count = int(input('Enter number of trains to simulate:\n'))
            if train_count < 1:
                raise ValueError
            else:
                train_catalog = Train.build_catalog(station_catalog, train_count)
            print('Simulation primed successfully. You may now choose a function.\n')
            loop = False
            simulation_menu(station_catalog, train_catalog)
        except ValueError:
            print('Input must be a positive integer. Please try again.\n')


if __name__ == '__main__':
    main()


"""
End of program.

"""
