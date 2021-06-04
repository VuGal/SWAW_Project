package com.example.weatherstation;

import android.content.res.Resources;
import android.os.StrictMode;
import android.support.constraint.ConstraintLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;

public class PredictionActivity extends AppCompatActivity {

    private Resources res;

    private TextView header_text;
    private TextView predicted_temperature_text;
    private TextView predicted_humidity_text;
    private TextView predicted_pressure_text;
    private TextView predicted_illuminance_text;
    private TextView predicted_precipitation_text;

    private Boolean is_night = false;

    private ConstraintLayout currentLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_prediction);

        res = getResources();

        currentLayout = findViewById(R.id.PredictionActivityLayout);

        //needed for thread actions
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        header_text = findViewById(R.id.text_header);
        predicted_temperature_text = findViewById(R.id.text_predicted_temperature);
        predicted_humidity_text = findViewById(R.id.text_predicted_humidity);
        predicted_pressure_text = findViewById(R.id.text_predicted_pressure);
        predicted_illuminance_text = findViewById(R.id.text_predicted_illuminance);
        predicted_precipitation_text = findViewById(R.id.text_predicted_precipitation);
        Button go_back_button = findViewById(R.id.go_back_button);
        Button day_night_button = findViewById(R.id.day_night_button);

        go_back_button.setOnClickListener(view -> goBack());
        day_night_button.setOnClickListener(view -> toggleDayNight());

        predicted_temperature_text.setText(res.getString(R.string.temperature_text, MainActivity.predicted_day_temperature_global));
        predicted_humidity_text.setText(res.getString(R.string.humidity_text, MainActivity.predicted_day_humidity_global));
        predicted_pressure_text.setText(res.getString(R.string.pressure_text, MainActivity.predicted_day_pressure_global));
        predicted_illuminance_text.setText(res.getString(R.string.illuminance_text, MainActivity.predicted_day_illuminance_global));
        if (MainActivity.predicted_day_precipitation_global.equals("0")) predicted_precipitation_text.setText(res.getString(R.string.precipitation_text, "NO"));
        else predicted_precipitation_text.setText(res.getString(R.string.precipitation_text, "YES"));

    }

    private void goBack() {

        super.onBackPressed();
        this.finish();

    }

    private void toggleDayNight() {

        is_night = !is_night;

        if (is_night == Boolean.TRUE) {

            currentLayout.setBackgroundColor(res.getColor(R.color.colorBackgroundNight));
            header_text.setTextColor(res.getColor(R.color.white));
            predicted_temperature_text.setTextColor(res.getColor(R.color.white));
            predicted_humidity_text.setTextColor(res.getColor(R.color.white));
            predicted_pressure_text.setTextColor(res.getColor(R.color.white));
            predicted_illuminance_text.setTextColor(res.getColor(R.color.white));
            predicted_precipitation_text.setTextColor(res.getColor(R.color.white));

            header_text.setText(R.string.prediction_header_night_text);

            predicted_temperature_text.setText(res.getString(R.string.temperature_text, MainActivity.predicted_night_temperature_global));
            predicted_humidity_text.setText(res.getString(R.string.humidity_text, MainActivity.predicted_night_humidity_global));
            predicted_pressure_text.setText(res.getString(R.string.pressure_text, MainActivity.predicted_night_pressure_global));
            predicted_illuminance_text.setText(res.getString(R.string.illuminance_text, MainActivity.predicted_night_illuminance_global));
            if (MainActivity.predicted_night_precipitation_global.equals("0")) predicted_precipitation_text.setText(res.getString(R.string.precipitation_text, "NO"));
            else predicted_precipitation_text.setText(res.getString(R.string.precipitation_text, "YES"));

        }
        else {

            currentLayout.setBackgroundColor(res.getColor(R.color.colorBackgroundStandard));
            header_text.setTextColor(res.getColor(R.color.black));
            predicted_temperature_text.setTextColor(res.getColor(R.color.black));
            predicted_humidity_text.setTextColor(res.getColor(R.color.black));
            predicted_pressure_text.setTextColor(res.getColor(R.color.black));
            predicted_illuminance_text.setTextColor(res.getColor(R.color.black));
            predicted_precipitation_text.setTextColor(res.getColor(R.color.black));

            header_text.setText(R.string.prediction_header_day_text);

            predicted_temperature_text.setText(res.getString(R.string.temperature_text, MainActivity.predicted_day_temperature_global));
            predicted_humidity_text.setText(res.getString(R.string.humidity_text, MainActivity.predicted_day_humidity_global));
            predicted_pressure_text.setText(res.getString(R.string.pressure_text, MainActivity.predicted_day_pressure_global));
            predicted_illuminance_text.setText(res.getString(R.string.illuminance_text, MainActivity.predicted_day_illuminance_global));
            if (MainActivity.predicted_day_precipitation_global.equals("0")) predicted_precipitation_text.setText(res.getString(R.string.precipitation_text, "NO"));
            else predicted_precipitation_text.setText(res.getString(R.string.precipitation_text, "YES"));

        }

    }

}