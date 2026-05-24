CREATE OR REPLACE FUNCTION fn_consulta_completa()
RETURNS TRIGGER AS $$
BEGIN

    INSERT INTO CONSULTA
    VALUES ( NEW.NUM_CON, NEW.FECHA_C, NEW.ESTATUS_C, NEW.NUM_COS, NEW.ID_SUCURSAL, NEW.ID_CEDULA );

    INSERT INTO HISTORIAL
    VALUES ( NEW.NUM_CON, NEW.CEDULA_ODO, NEW.FECHA_C, NEW.FECHA_C + INTERVAL '5 days', NEW.ID_PAGO, NEW.NOM_T );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRG_CONSULTA_COMPLETA
AFTER INSERT ON CONSULTA_COMPLETA
FOR EACH ROW
EXECUTE FUNCTION fn_consulta_completa();

-- REGISTRAR PACIENTE

CREATE OR REPLACE PROCEDURE registrar_paciente(
    p_num_a            INTEGER,
    p_tipoafiliado     VARCHAR(15),
    p_costo_m          NUMERIC(6,2),

    p_id_cedula        INTEGER,
    p_nomp             VARCHAR(30),
    p_app              VARCHAR(30),
    p_amp              VARCHAR(30),
    p_monto_mensual    NUMERIC(6,2),

    p_telefono         BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN

    INSERT INTO AFILIADO( NUM_A, TIPOAFILIADO, COSTO_M)
    VALUES( p_num_a, UPPER(p_tipoafiliado), p_costo_m );

    INSERT INTO PACIENTE( ID_CEDULA, NOMP, APP, AMP, MONTO_MENSUAL, NUM_A )
    VALUES( p_id_cedula, p_nomp, p_app, p_amp, p_monto_mensual, p_num_a);

    INSERT INTO TELEFONO_P( TELEFONO, ID_CEDULA )
    VALUES( p_telefono, p_id_cedula);

END;
$$;


-- GENERAR PAGO

CREATE OR REPLACE PROCEDURE generar_pago(
    p_id_pago      INTEGER,
    p_fecha_pago   TIMESTAMP,
    p_monto        NUMERIC(6,2)
)
LANGUAGE plpgsql
AS $$
BEGIN

    INSERT INTO PAGO( ID_PAGO, FECHA_PAGO, MONTO)
    VALUES( p_id_pago, p_fecha_pago, p_monto);

END;
$$;

-- ASIGNAR ODONTOLOGO

CREATE OR REPLACE PROCEDURE asignar_odontologo(
    p_num_con      INTEGER,
    p_cedula_odo   INTEGER,
    p_fecha_it     TIMESTAMP,
    p_fecha_ft     TIMESTAMP,
    p_id_pago      INTEGER,
    p_nom_t        VARCHAR(10)
)
LANGUAGE plpgsql
AS $$
BEGIN

    INSERT INTO HISTORIAL( NUM_CON, CEDULA, FECHA_IT, FECHA_FT, ID_PAGO, NOM_T)
    VALUES( p_num_con, p_cedula_odo, p_fecha_it, p_fecha_ft, p_id_pago, p_nom_t );

END;
$$;

-- CREAR CONSULTA

CREATE OR REPLACE PROCEDURE crear_consulta(
    p_num_con        INTEGER,
    p_fecha_c        TIMESTAMP,
    p_estatus_c      VARCHAR(10),
    p_num_cos        INTEGER,
    p_id_sucursal    INTEGER,
    p_id_cedula      INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN

    INSERT INTO CONSULTA( NUM_CON, FECHA_C, ESTATUS_C, NUM_COS, ID_SUCURSAL, ID_CEDULA )
    VALUES( p_num_con, p_fecha_c, UPPER(p_estatus_c), p_num_cos, p_id_sucursal, p_id_cedula );

END;
$$;
