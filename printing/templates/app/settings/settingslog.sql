INSERT INTO settings_log (
        `settingsID`,
        `old_row_data`,
        `new_row_data`,
        `type`,
        `timestamp`,
        `created_by`
   )
    VALUES(
        OLD.id,
        JSON_OBJECT(
            "cost_kW", OLD.cost_kW,
            "default_markup", OLD.default_markup,
            "default_discount", OLD.default_discount,
            "padding_time", OLD.padding_time,
            "padding_filament", OLD.padding_filament
        ),
        JSON_OBJECT(
            "cost_kW", NEW.cost_kW,
            "default_markup", NEW.default_markup,
            "default_discount", NEW.default_discount,
            "padding_time", NEW.padding_time,
            "padding_filament", NEW.padding_filament
        ),
        'UPDATE',
        CURRENT_TIMESTAMP,
        USER()
    )