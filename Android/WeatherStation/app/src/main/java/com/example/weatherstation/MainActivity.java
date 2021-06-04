package com.example.weatherstation;

import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Resources;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {

    public static final String SHARED_PREFS = "sharedPrefs";
    public static final String IP_ADDRESS = "0.0.0.0";

    private Resources res;

    public static String predicted_day_temperature_global = "";
    public static String predicted_night_temperature_global = "";
    public static String predicted_day_humidity_global = "";
    public static String predicted_night_humidity_global = "";
    public static String predicted_day_pressure_global = "";
    public static String predicted_night_pressure_global = "";
    public static String predicted_day_illuminance_global = "";
    public static String predicted_night_illuminance_global = "";
    public static String predicted_day_precipitation_global = "";
    public static String predicted_night_precipitation_global = "";

    private Boolean error_flag = false;
    private String ip_address = "";
    private TextView temperature_text;
    private TextView humidity_text;
    private TextView pressure_text;
    private TextView illuminance_text;

    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        res = getResources();

        //load saved data from device memory
        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREFS, MODE_PRIVATE);
        ip_address = sharedPreferences.getString(IP_ADDRESS, "23.102.182.59");

        //needed for thread actions
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        temperature_text = findViewById(R.id.text_temperature);
        humidity_text = findViewById(R.id.text_humidity);
        pressure_text = findViewById(R.id.text_pressure);
        illuminance_text = findViewById(R.id.text_illuminance);
        Button update_button = findViewById(R.id.update_button);
        Button prediction_button = findViewById(R.id.prediction_button);

        updateData();

        update_button.setOnClickListener(view -> updateData());
        prediction_button.setOnClickListener(view -> showPrediction());

    }

    private void updateData() {

        new Thread(() -> {

        final StringBuilder current_temperature_builder = new StringBuilder();
        final StringBuilder predicted_day_temperature_builder = new StringBuilder();
        final StringBuilder predicted_night_temperature_builder = new StringBuilder();
        final StringBuilder current_humidity_builder = new StringBuilder();
        final StringBuilder predicted_day_humidity_builder = new StringBuilder();
        final StringBuilder predicted_night_humidity_builder = new StringBuilder();
        final StringBuilder current_pressure_builder = new StringBuilder();
        final StringBuilder predicted_day_pressure_builder = new StringBuilder();
        final StringBuilder predicted_night_pressure_builder = new StringBuilder();
        final StringBuilder current_illuminance_builder = new StringBuilder();
        final StringBuilder predicted_day_illuminance_builder = new StringBuilder();
        final StringBuilder predicted_night_illuminance_builder = new StringBuilder();
        final StringBuilder predicted_day_precipitation_builder = new StringBuilder();
        final StringBuilder predicted_night_precipitation_builder = new StringBuilder();

            try {

                // fetching current data
                Document doc = Jsoup.connect("http://" + ip_address + "/index.html").get();

                Elements current_temperature = doc.select("div#Temperature");
                Elements humidity = doc.select("div#Humidity");
                Elements pressure = doc.select("div#Pressure");
                Elements illuminance = doc.select("div#Illuminance");

                current_temperature_builder.append(current_temperature.text());
                current_humidity_builder.append(humidity.text());
                current_pressure_builder.append(pressure.text());
                current_illuminance_builder.append(illuminance.text());


                // fetching predicted data
                doc = Jsoup.connect("http://" + ip_address + "/index2.html").get();

                Elements predicted_day_temperature = doc.select("div#TemperatureDay");
                Elements predicted_night_temperature = doc.select("div#TemperatureNight");
                Elements predicted_day_humidity = doc.select("div#HumidityDay");
                Elements predicted_night_humidity = doc.select("div#HumidityNight");
                Elements predicted_day_pressure = doc.select("div#PressureDay");
                Elements predicted_night_pressure = doc.select("div#PressureNight");
                Elements predicted_day_illuminance = doc.select("div#IlluminanceDay");
                Elements predicted_night_illuminance = doc.select("div#IlluminanceNight");
                Elements predicted_day_precipitation = doc.select("div#PrecipitationDay");
                Elements predicted_night_precipitation = doc.select("div#PrecipitationNight");

                predicted_day_temperature_global = predicted_day_temperature.text();
                predicted_night_temperature_global = predicted_night_temperature.text();
                predicted_day_humidity_global = predicted_day_humidity.text();
                predicted_night_humidity_global = predicted_night_humidity.text();
                predicted_day_pressure_global = predicted_day_pressure.text();
                predicted_night_pressure_global = predicted_night_pressure.text();
                predicted_day_illuminance_global = predicted_day_illuminance.text();
                predicted_night_illuminance_global = predicted_night_illuminance.text();
                predicted_day_precipitation_global = predicted_day_precipitation.text();
                predicted_night_precipitation_global = predicted_night_precipitation.text();

                predicted_day_temperature_builder.append(predicted_day_temperature.text());
                predicted_night_temperature_builder.append(predicted_night_temperature.text());
                predicted_day_humidity_builder.append(predicted_day_humidity.text());
                predicted_night_humidity_builder.append(predicted_night_humidity.text());
                predicted_day_pressure_builder.append(predicted_day_pressure.text());
                predicted_night_pressure_builder.append(predicted_night_pressure.text());
                predicted_day_illuminance_builder.append(predicted_day_illuminance.text());
                predicted_night_illuminance_builder.append(predicted_night_illuminance.text());
                predicted_day_precipitation_builder.append(predicted_day_precipitation.text());
                predicted_night_precipitation_builder.append(predicted_night_precipitation.text());

                error_flag = false;

            } catch (IOException e) {
                error_flag = true;
            }

            runOnUiThread(() -> {
                if(!error_flag) { //if there is no error

                    temperature_text.setText(res.getString(R.string.temperature_text, current_temperature_builder.toString()));
                    humidity_text.setText(res.getString(R.string.humidity_text, current_humidity_builder.toString()));
                    pressure_text.setText(res.getString(R.string.pressure_text, current_pressure_builder.toString()));
                    illuminance_text.setText(res.getString(R.string.illuminance_text, current_illuminance_builder.toString()));

                }
                else {
                    Log.e(TAG, "ERROR");
                }
            });
        }).start();

    }

    private void showPrediction() {
        Intent intent = new Intent(this, PredictionActivity.class);
        startActivity(intent);
    }

}