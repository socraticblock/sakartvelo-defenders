## GridMap — Isometric grid system for tower placement
## Converts between screen coordinates and grid coordinates
extends Node2D

signal tower_requested(grid_pos: Vector2i, tower_type: String)

@export var grid_width: int = 16
@export var grid_height: int = 12
@export var cell_size: float = 64.0  # pixels per cell in isometric

## Grid data: 0=empty, 1=path, 2=tower, 3=blocked
var grid: Array = []
var towers: Dictionary = {}  # Vector2i -> Tower node

## Path waypoints in grid coordinates (set per level)
var path_waypoints: Array[Vector2i] = []
var path_set: Array = []  # All grid cells that are path

func _ready() -> void:
	_init_grid()

func _init_grid() -> void:
	grid.clear()
	for y in range(grid_height):
		var row: Array = []
		row.resize(grid_width)
		row.fill(0)
		grid.append(row)

## Convert grid coordinates to isometric screen position
func grid_to_world(gpos: Vector2i) -> Vector2:
	var x: float = (gpos.x - gpos.y) * cell_size * 0.5
	var y: float = (gpos.x + gpos.y) * cell_size * 0.25
	return Vector2(x, y) + global_position

## Convert screen position to grid coordinates
func world_to_grid(world_pos: Vector2) -> Vector2i:
	var local: Vector2 = world_pos - global_position
	var gx: float = (local.x / (cell_size * 0.5) + local.y / (cell_size * 0.25)) * 0.5
	var gy: float = (local.y / (cell_size * 0.25) - local.x / (cell_size * 0.5)) * 0.5
	return Vector2i(int(floor(gx)), int(floor(gy)))

## Check if grid position is valid and empty
func is_valid_placement(gpos: Vector2i) -> bool:
	if gpos.x < 0 or gpos.x >= grid_width or gpos.y < 0 or gpos.y >= grid_height:
		return false
	return grid[gpos.y][gpos.x] == 0

## Set a grid cell as path
func set_path_cell(gpos: Vector2i) -> void:
	if _in_bounds(gpos):
		grid[gpos.y][gpos.x] = 1
		if gpos not in path_set:
			path_set.append(gpos)

## Place a tower on the grid
func place_tower(gpos: Vector2i, tower_type: String) -> bool:
	if not is_valid_placement(gpos):
		return false
	grid[gpos.y][gpos.x] = 2
	print("[GridMap] Tower '%s' placed at (%d, %d)" % [tower_type, gpos.x, gpos.y])
	return true

## Remove a tower from the grid
func remove_tower(gpos: Vector2i) -> void:
	if _in_bounds(gpos):
		grid[gpos.y][gpos.x] = 0
		towers.erase(gpos)

## Set the path from waypoints (fills path cells between waypoints)
func set_path_from_waypoints(waypoints: Array[Vector2i]) -> void:
	path_waypoints = waypoints
	for wp in waypoints:
		set_path_cell(wp)
	
	# Fill cells between consecutive waypoints
	for i in range(waypoints.size() - 1):
		var from: Vector2i = waypoints[i]
		var to: Vector2i = waypoints[i + 1]
		_fill_path_between(from, to)

func _fill_path_between(from: Vector2i, to: Vector2i) -> void:
	# Simple: step through cells along the line
	var dx: int = signi(to.x - from.x)
	var dy: int = signi(to.y - from.y)
	var cx: int = from.x
	var cy: int = from.y
	
	while cx != to.x or cy != to.y:
		set_path_cell(Vector2i(cx, cy))
		if cx != to.x:
			cx += dx
		if cy != to.y:
			cy += dy
	set_path_cell(to)

## Get the world-space path for enemies to follow
func get_world_path() -> Array[Vector2]:
	var result: Array[Vector2] = []
	for wp in path_waypoints:
		result.append(grid_to_world(wp))
	return result

func _in_bounds(gpos: Vector2i) -> bool:
	return gpos.x >= 0 and gpos.x < grid_width and gpos.y >= 0 and gpos.y < grid_height

## Draw debug grid (visible in editor for testing)
func _draw() -> void:
	# Draw grid lines
	for y in range(grid_height + 1):
		for x in range(grid_width + 1):
			var p: Vector2 = grid_to_world(Vector2i(x, y))
			# Draw cell markers for path/tower
			if x < grid_width and y < grid_height:
				var cell_val: int = grid[y][x] if y < grid.size() and x < grid[y].size() else 0
				var color: Color
				match cell_val:
					0: color = Color(1, 1, 1, 0.05)  # Empty — barely visible
					1: color = Color(0.6, 0.4, 0.2, 0.3)  # Path — brown
					2: color = Color(0.2, 0.6, 0.2, 0.3)  # Tower — green
					_: color = Color(1, 0, 0, 0.2)
				var p1: Vector2 = grid_to_world(Vector2i(x, y))
				var p2: Vector2 = grid_to_world(Vector2i(x + 1, y))
				var p3: Vector2 = grid_to_world(Vector2i(x + 1, y + 1))
				var p4: Vector2 = grid_to_world(Vector2i(x, y + 1))
				draw_colored_polygon([p1, p2, p3, p4], color)
