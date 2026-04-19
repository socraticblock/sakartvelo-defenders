## WaveManager — Spawns enemy waves along the path
extends Node

@export var spawn_interval: float = 1.2

var grid_map: Node2D
var spawn_timer: float = 0.0
var enemies_to_spawn: int = 0
var is_spawning: bool = false

func _ready() -> void:
	GameManager.wave_started.connect(_on_wave_started)

func _process(delta: float) -> void:
	if not is_spawning:
		return
	spawn_timer -= delta
	if spawn_timer <= 0.0 and enemies_to_spawn > 0:
		_spawn_enemy()
		spawn_timer = spawn_interval

func _on_wave_started(wave_num: int) -> void:
	enemies_to_spawn = GameManager.get_wave_enemy_count()
	is_spawning = true
	spawn_timer = 0.5
	print("[Wave] Wave %d: %d enemies incoming" % [wave_num, enemies_to_spawn])

func _spawn_enemy() -> void:
	if not grid_map:
		return
	
	# Create enemy
	var enemy := CharacterBody2D.new()
	enemy.set_script(load("res://scripts/enemies/enemy.gd"))
	
	# Add to scene
	grid_map.get_parent().add_child(enemy)
	
	# Set path
	var world_path: Array = grid_map.get_world_path()
	enemy.set_path(world_path)
	
	if world_path.size() > 0:
		enemy.global_position = world_path[0]
	
	enemies_to_spawn -= 1
	if enemies_to_spawn <= 0:
		is_spawning = false
		print("[Wave] All spawned for wave %d" % GameManager.current_wave)
