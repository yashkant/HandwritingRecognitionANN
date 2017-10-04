package com.ariesiitr.developer.ocr;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Environment;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Toast;
import com.afollestad.materialcamera.MaterialCamera;
import java.io.File;
import java.text.DecimalFormat;

/** @author Aidan Follestad (afollestad) */
public class MainActivity extends AppCompatActivity implements View.OnClickListener {

  private static final int CAMERA_RQ = 6969;
  private static final int PERMISSION_RQ = 84;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    setContentView(R.layout.activity_main);
    findViewById(R.id.launchCamera).setOnClickListener(this);
    findViewById(R.id.launchCameraStillshot).setOnClickListener(this);
    findViewById(R.id.launchFromFragment).setOnClickListener(this);
    findViewById(R.id.launchFromFragmentSupport).setOnClickListener(this);

    if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
        != PackageManager.PERMISSION_GRANTED) {
      // Request permission to save videos in external storage
      ActivityCompat.requestPermissions(
          this, new String[] {Manifest.permission.WRITE_EXTERNAL_STORAGE}, PERMISSION_RQ);
    }
  }

  @SuppressWarnings("ResultOfMethodCallIgnored")
  @Override
  public void onClick(View view) {
    if (view.getId() == R.id.launchFromFragment) {
      Intent intent = new Intent(this, FragmentActivity.class);
      startActivity(intent);
      return;
    }
    if (view.getId() == R.id.launchFromFragmentSupport) {
      Intent intent = new Intent(this, FragmentActivity.class);
      intent.putExtra("support", true);
      startActivity(intent);
      return;
    }

    File saveDir = null;

    if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
        == PackageManager.PERMISSION_GRANTED) {
      // Only use external storage directory if permission is granted, otherwise cache directory is used by default
      saveDir = new File(Environment.getExternalStorageDirectory(), "MaterialCamera");
      saveDir.mkdirs();
    }

    MaterialCamera materialCamera =
        new MaterialCamera(this)
            .saveDir(saveDir)
            .showPortraitWarning(true)
            .allowRetry(true)
            .defaultToFrontFacing(true)
            .allowRetry(true)
            .autoSubmit(false)
            .labelConfirm(R.string.mcam_use_video);

    if (view.getId() == R.id.launchCameraStillshot)
      materialCamera
          .stillShot() // launches the Camera in stillshot mode
          .labelConfirm(R.string.mcam_use_stillshot);
    materialCamera.start(CAMERA_RQ);
  }

  private String readableFileSize(long size) {
    if (size <= 0) return size + " B";
    final String[] units = new String[] {"B", "KB", "MB", "GB", "TB"};
    int digitGroups = (int) (Math.log10(size) / Math.log10(1024));
    return new DecimalFormat("#,##0.##").format(size / Math.pow(1024, digitGroups))
        + " "
        + units[digitGroups];
  }

  private String fileSize(File file) {
    return readableFileSize(file.length());
  }

  @Override
  protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    super.onActivityResult(requestCode, resultCode, data);

    // Received recording or error from MaterialCamera
    if (requestCode == CAMERA_RQ) {
      if (resultCode == RESULT_OK) {
        final File file = new File(data.getData().getPath());
        Toast.makeText(
                this,
                String.format("Saved to: %s, size: %s", file.getAbsolutePath(), fileSize(file)),
                Toast.LENGTH_LONG)
            .show();
      } else if (data != null) {
        Exception e = (Exception) data.getSerializableExtra(MaterialCamera.ERROR_EXTRA);
        if (e != null) {
          e.printStackTrace();
          Toast.makeText(this, "Error: " + e.getMessage(), Toast.LENGTH_LONG).show();
        }
      }
    }
  }

  @Override
  public void onRequestPermissionsResult(
      int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
    super.onRequestPermissionsResult(requestCode, permissions, grantResults);

    if (grantResults[0] != PackageManager.PERMISSION_GRANTED) {
      // Sample was denied WRITE_EXTERNAL_STORAGE permission
      Toast.makeText(
              this,
              "Videos will be saved in a cache directory instead of an external storage directory since permission was denied.",
              Toast.LENGTH_LONG)
          .show();
    }
  }
}