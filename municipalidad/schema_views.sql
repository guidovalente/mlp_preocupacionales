-- agentes_pendientes
create view
	agentes_pendientes
as
	select
		a.tipo as tipo_turno,
		agentes.id,
		agentes.nombre,
		agentes.apellido,
		agentes.dni,
		agentes.legajo,
		agentes.reparticion_id,
		agentes.apto_psi,
		agentes.apto_med
	from (
			select
				agente_id,
				tipo,
				numero,
				max(fecha) as fecha
			from
				turnos
			group by
				agente_id,
				tipo
			order by
				agente_id) a
		inner join agentes on agentes.id = a.agente_id
	where
		a.fecha is null
		and ( agentes.apto_med = 0 or agentes.apto_psi = 0)
