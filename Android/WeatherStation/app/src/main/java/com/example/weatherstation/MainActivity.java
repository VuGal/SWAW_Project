package com.example.weatherstation;

import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {

    public static final String SHARED_PREFS = "sharedPrefs";
    public static final String IP_ADDRESS = "0.0.0.0";

    private Boolean error_flag = false;
    private String ip_address = "";
    private TextView temperature_text;
    private TextView humidity_text;
    private TextView pressure_text;
    private TextView illuminance_text;
    private Button update_button;

    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

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
        update_button = findViewById(R.id.update_button);

        checkWebsite();

        update_button.setOnClickListener(view -> checkWebsite());

    }

    private void checkWebsite() {

        new Thread(() -> {

        final StringBuilder temperature_builder = new StringBuilder();
        final StringBuilder humidity_builder = new StringBuilder();
        final StringBuilder pressure_builder = new StringBuilder();
        final StringBuilder illuminance_builder = new StringBuilder();
            try {

                Document doc = Jsoup.connect("http://" + ip_address + "/").get();   //connects to the main website and set its text to the current fuse state

                Elements temperature = doc.select("div#Temperature");
                temperature_builder.append(temperature.text());

                Elements humidity = doc.select("div#Humidity");
                humidity_builder.append(humidity.text());

                Elements pressure = doc.select("div#Pressure");
                pressure_builder.append(pressure.text());

                Elements illuminance = doc.select("div#Illuminance");
                illuminance_builder.append(illuminance.text());

                error_flag = false;

            } catch (IOException e) {
                error_flag = true;
            }

            runOnUiThread(() -> {
                if(error_flag == false) { //if there is no error

                    temperature_text.setText("Temperature: " + temperature_builder.toString() + " °C");
                    humidity_text.setText("Humidity: " + humidity_builder.toString() + " %");
                    pressure_text.setText("Pressure: " + pressure_builder.toString() + " hPa");
                    illuminance_text.setText("Illuminance: " + illuminance_builder.toString() + " Lx");

                }
                else {
                    Log.e(TAG, "ERROR");
                }
            });
        }).start();


    }
}