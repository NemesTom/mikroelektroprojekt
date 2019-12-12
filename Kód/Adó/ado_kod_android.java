package lazernet.lilikferenc.dev.com.pycar_controller;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.StrictMode;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.NetworkInterface;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    Button connectButton;
    Button sendWButton;
    Button sendSButton;
    Button sendAButton;
    Button sendDButton;
    Button lampButton;
    Button powerButton;
    EditText ipInput;
    TextView logoText;
    TextView nameText;
    ImageView car_plan;
    ImageView arrow_forward;
    ImageView arrow_backward;
    ImageView arrow_left;
    ImageView arrow_right;
    Socket s;
    boolean lamp=true;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        setContentView(R.layout.activity_main);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        connectButton=findViewById(R.id.connectButton);
        ipInput=findViewById(R.id.ipInput);
        sendWButton=findViewById(R.id.sendW);
        sendSButton=findViewById(R.id.sendS);
        sendAButton=findViewById(R.id.sendA);
        sendDButton=findViewById(R.id.sendD);
        logoText=findViewById(R.id.logoText);
        nameText=findViewById(R.id.nameText);
        car_plan=findViewById(R.id.car_plan);
        powerButton=findViewById(R.id.powerButton);
        lampButton=findViewById(R.id.lampButton);
        arrow_forward=findViewById(R.id.car_forward);
        arrow_backward=findViewById(R.id.car_backward);
        arrow_left=findViewById(R.id.car_left);
        arrow_right=findViewById(R.id.car_right);

            lampButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if(lamp){
                        lamp=false;
                    }else{
                        lamp=true;
                    }
                }
            });

            connectButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    final String ipString=ipInput.getText().toString();
                        final Handler h = new Handler();
                        final Thread r = new Thread(new Runnable() {
                            public void run() {
                                try{
                                    s = new Socket(ipString, 8080);
                                    sendAButton.setVisibility(View.VISIBLE);
                                    sendDButton.setVisibility(View.VISIBLE);
                                    sendWButton.setVisibility(View.VISIBLE);
                                    sendSButton.setVisibility(View.VISIBLE);
                                    nameText.setVisibility(View.VISIBLE);
                                    logoText.setVisibility(View.VISIBLE);
                                    car_plan.setVisibility(View.VISIBLE);
                                    lampButton.setVisibility(View.VISIBLE);
                                    powerButton.setVisibility(View.VISIBLE);
                                    ipInput.setVisibility(View.GONE);
                                    connectButton.setVisibility(View.GONE);
                                    final Runnable [] runnables = new Runnable[1];
                                    final Handler senderHandler=new Handler();
                                    runnables[0] = new Runnable() {
                                        @Override
                                        public void run() {
                                            try{
                                                final DataOutputStream dOut = new DataOutputStream(s.getOutputStream());
                                                    boolean isEmpty=true;
                                                    if (sendAButton.isPressed()) {
                                                        dOut.writeChar('a');
                                                        dOut.flush();
                                                        isEmpty=false;
                                                        h.post(new Runnable() {
                                                            @Override
                                                            public void run() {
                                                                arrow_right.setVisibility(View.GONE);
                                                                arrow_left.setVisibility(View.VISIBLE);
                                                            }
                                                        });
                                                    }else if (sendDButton.isPressed()) {
                                                        dOut.writeChar('d');
                                                        dOut.flush();
                                                        isEmpty=false;
                                                        h.post(new Runnable() {
                                                            @Override
                                                            public void run() {
                                                                arrow_right.setVisibility(View.VISIBLE);
                                                                arrow_left.setVisibility(View.GONE);
                                                            }
                                                        });
                                                    }else{
                                                        h.post(new Runnable() {
                                                            @Override
                                                            public void run() {
                                                                arrow_right.setVisibility(View.GONE);
                                                                arrow_left.setVisibility(View.GONE);
                                                            }
                                                        });
                                                    }
                                                    if (sendWButton.isPressed()) {
                                                        dOut.writeChar('w');
                                                        dOut.flush();
                                                        isEmpty=false;
                                                        h.post(new Runnable() {
                                                            @Override
                                                            public void run() {
                                                                arrow_backward.setVisibility(View.GONE);
                                                                arrow_forward.setVisibility(View.VISIBLE);
                                                            }
                                                        });
                                                    }else if (sendSButton.isPressed()) {
                                                        dOut.writeChar('s');
                                                        dOut.flush();
                                                        isEmpty=false;
                                                        h.post(new Runnable() {
                                                            @Override
                                                            public void run() {
                                                                arrow_forward.setVisibility(View.GONE);
                                                                arrow_backward.setVisibility(View.VISIBLE);
                                                            }
                                                        });
                                                    }else{
                                                        h.post(new Runnable() {
                                                            @Override
                                                            public void run() {
                                                                arrow_forward.setVisibility(View.GONE);
                                                                arrow_backward.setVisibility(View.GONE);
                                                            }
                                                        });
                                                    }

                                                    if(lamp){
                                                        dOut.writeChar(('o'));
                                                        dOut.flush();
                                                    }else{
                                                        dOut.writeChar(('n'));
                                                        dOut.flush();
                                                    }

                                                    if(isEmpty){
                                                        dOut.writeChar('x');
                                                        dOut.flush();
                                                    }

                                                    if(powerButton.isPressed()){
                                                        dOut.writeChar('q');
                                                        dOut.flush();
                                                        System.exit(0);
                                                    }

                                            }catch (Exception ex){}
                                            senderHandler.postDelayed(runnables[0], 0);
                                        }
                                    };
                                    senderHandler.post(runnables[0]);
                                }catch (final Exception ex){
                                    h.post(new Runnable() {
                                        @Override
                                        public void run() {
                                            Toast.makeText(getApplicationContext(),ex.toString(),Toast.LENGTH_LONG).show();
                                        }
                                    });
                                }
                            }
                            });
                        r.run();
                }
            });
    }
}

