## GameManager — Global autoload singleton
## Manages game state: gold, lives, wave, era
extends Node

signal gold_changed(new_amount: int)
signal lives_changed(new_amount: int)
signal wave_changed(wave_num: int, total_waves: int)
signal game_over(won: bool)
signal wave_started(wave_num: int)
signal wave_completed(wave_num: int)

## Game state
var gold: int = 100:
	set(v):
		gold = maxi(v, 0)
		gold_changed.emit(gold)

var lives: int = 20:
	set(v):
		lives = v
		lives_changed.emit(lives)
		if lives <= 0:
			game_over.emit(false)

var current_wave: int = 0
var total_waves: int = 5
var current_era: int = 0
var current_level: int = 0
var enemies_alive: int = 0
var enemies_spawned: int = 0
var is_wave_active: bool = false
var is_build_phase: bool = true

## Tower costs
const TOWER_COSTS := {
	"archer": 50,
	"catapult": 100,
	"wall": 25,
}

func _ready() -> void:
	print("[GameManager] Ready — Era %d, Level %d" % [current_era, current_level])

func start_wave() -> void:
	if is_wave_active:
		return
	is_wave_active = true
	is_build_phase = false
	current_wave += 1
	wave_changed.emit(current_wave, total_waves)
	wave_started.emit(current_wave)
	print("[GameManager] Wave %d/%d started" % [current_wave, total_waves])

func complete_wave() -> void:
	is_wave_active = false
	is_build_phase = true
	wave_completed.emit(current_wave)
	gold += 25 + current_wave * 10  # Wave completion bonus
	print("[GameManager] Wave %d complete. Gold: %d" % [current_wave, gold])
	
	if current_wave >= total_waves:
		game_over.emit(true)
		print("[GameManager] Level complete!")

func enemy_killed(reward: int = 10) -> void:
	gold += reward
	enemies_alive -= 1
	print("[GameManager] Enemy killed. +%d gold (total: %d, alive: %d)" % [reward, gold, enemies_alive])
	
	if enemies_alive <= 0 and enemies_spawned >= get_wave_enemy_count():
		complete_wave()

func enemy_reached_end() -> void:
	lives -= 1
	enemies_alive -= 1
	print("[GameManager] Enemy reached end! Lives: %d" % lives)
	
	if enemies_alive <= 0 and enemies_spawned >= get_wave_enemy_count():
		complete_wave()

func register_enemy() -> void:
	enemies_alive += 1
	enemies_spawned += 1

func get_wave_enemy_count() -> int:
	# Simple scaling: more enemies each wave
	return 5 + current_wave * 3

func can_afford(tower_type: String) -> bool:
	return gold >= TOWER_COSTS.get(tower_type, 999)

func spend_gold(amount: int) -> void:
	gold -= amount

func reset_for_level() -> void:
	gold = 100
	lives = 20
	current_wave = 0
	enemies_alive = 0
	enemies_spawned = 0
	is_wave_active = false
	is_build_phase = true
