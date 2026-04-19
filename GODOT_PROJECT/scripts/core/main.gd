## Main — Root scene: sets up level, wires nodes together
extends Node2D

@export var level_era: int = 0
@export var level_num: int = 1
@export var total_waves: int = 5
@export var starting_gold: int = 100
@export var starting_lives: int = 20

var grid_map: Node2D
var wave_manager: Node
var hud: CanvasLayer
var tower_container: Node2D

func _ready() -> void:
	print("\n" + "=" .repeat(40))
	print("  SAKARTVELO DEFENDERS")
	print("  Era %d — Level %d" % [level_era, level_num])
	print("=" .repeat(40))
	
	_init_game_state()
	_build_scene()
	_setup_level_path()
	_setup_camera()
	
	print("[Main] Ready. Build phase — place your towers!\n")

func _init_game_state() -> void:
	GameManager.current_era = level_era
	GameManager.current_level = level_num
	GameManager.total_waves = total_waves
	GameManager.gold = starting_gold
	GameManager.lives = starting_lives
	GameManager.current_wave = 0
	GameManager.enemies_alive = 0
	GameManager.enemies_spawned = 0
	GameManager.is_wave_active = false
	GameManager.is_build_phase = true

func _build_scene() -> void:
	# Grid map
	grid_map = Node2D.new()
	grid_map.set_script(load("res://scripts/core/grid_map.gd"))
	grid_map.grid_width = 16
	grid_map.grid_height = 12
	grid_map.cell_size = 64.0
	add_child(grid_map)
	
	# Tower container (so towers are above grid in z-order)
	tower_container = Node2D.new()
	tower_container.name = "Towers"
	add_child(tower_container)
	
	# Wave manager
	wave_manager = Node.new()
	wave_manager.set_script(load("res://scripts/core/wave_manager.gd"))
	wave_manager.grid_map = grid_map
	add_child(wave_manager)
	
	# HUD (top layer)
	hud = CanvasLayer.new()
	hud.set_script(load("res://scripts/ui/hud.gd"))
	hud.grid_map = grid_map
	add_child(hud)

func _setup_level_path() -> void:
	# Era 0, Level 1: S-curve through Colchian lowlands
	# Enemies enter from left, zigzag across the map, exit right
	var waypoints: Array[Vector2i] = [
		Vector2i(0, 3),
		Vector2i(5, 3),
		Vector2i(5, 8),
		Vector2i(10, 8),
		Vector2i(10, 3),
		Vector2i(15, 3),
	]
	grid_map.set_path_from_waypoints(waypoints)
	grid_map.queue_redraw()

func _setup_camera() -> void:
	var camera := Camera2D.new()
	var center: Vector2 = grid_map.grid_to_world(Vector2i(8, 6))
	camera.position = center
	camera.zoom = Vector2(1.0, 1.0)
	add_child(camera)
	camera.make_current()

## Public: place a tower (called by HUD)
func place_tower_at(gpos: Vector2i, tower_type: String) -> bool:
	if not grid_map.is_valid_placement(gpos):
		return false
	if not GameManager.can_afford(tower_type):
		return false
	
	var cost: int = GameManager.TOWER_COSTS.get(tower_type, 999)
	if not grid_map.place_tower(gpos, tower_type):
		return false
	
	GameManager.spend_gold(cost)
	
	var tower := Node2D.new()
	tower.set_script(load("res://scripts/towers/tower.gd"))
	tower.tower_type = tower_type
	tower.grid_pos = gpos
	tower.global_position = grid_map.grid_to_world(gpos)
	
	# Type-specific stats
	match tower_type:
		"archer":
			tower.damage = 15.0
			tower.attack_range = 150.0
			tower.attack_speed = 1.0
			tower.projectile_speed = 300.0
		"catapult":
			tower.damage = 45.0
			tower.attack_range = 220.0
			tower.attack_speed = 0.35
			tower.projectile_speed = 180.0
		"wall":
			tower.damage = 0.0
			tower.attack_range = 0.0
			tower.attack_speed = 0.0
	
	tower_container.add_child(tower)
	grid_map.towers[gpos] = tower
	grid_map.queue_redraw()
	
	print("[Main] Placed %s at (%d,%d) for %dg" % [tower_type, gpos.x, gpos.y, cost])
	return true
