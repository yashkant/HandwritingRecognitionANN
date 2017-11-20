package com.ariesiitr.developer.ocr;

import android.Manifest;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Toast;
import com.afollestad.materialcamera.MaterialCamera;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import android.net.Uri;
import java.net.URL;
import java.net.URLEncoder;
import java.text.DecimalFormat;
import java.util.HashMap;
import java.util.Map;

import javax.net.ssl.HttpsURLConnection;

/** @author Aidan Follestad (afollestad) */
public class MainActivity extends AppCompatActivity implements View.OnClickListener {
  String ConvertImage;
  private static final int CAMERA_RQ = 6969;
  private static final int PERMISSION_RQ = 84;
  ProgressDialog progressDialog ;
  Bitmap bitmap;

  boolean check = true;
  String GetImageNameEditText="ImageOfUse";

  String ImageName = "image_name" ;

  String ImagePath = "image_path" ;

  String ServerUploadPath ="https://droidwar.000webhostapp.com/ImageUpload.php" ;
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
        Uri uri = data.getData();
        try {
          bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), uri);
          ImageUploadToServerFunction();
          Log.e("this", "Image upload function called 2");
        } catch (IOException e) {
          e.printStackTrace();
        }

//        imageView.setImageBitmap(bitmap);

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
  public void ImageUploadToServerFunction(){
    Log.e("this", "Image upload function called 1");

    ByteArrayOutputStream byteArrayOutputStreamObject ;

    byteArrayOutputStreamObject = new ByteArrayOutputStream();

    bitmap.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStreamObject);

    byte[] byteArrayVar = byteArrayOutputStreamObject.toByteArray();

     ConvertImage = Base64.encodeToString(byteArrayVar, Base64.DEFAULT);


    AsyncTaskUploadClass AsyncTaskUploadClassOBJ = new AsyncTaskUploadClass();

    AsyncTaskUploadClassOBJ.execute();
  }
  class AsyncTaskUploadClass extends AsyncTask<Void,Void,String> {

    @Override
    protected void onPreExecute() {

      super.onPreExecute();
//        progressDialog= new ProgressDialog(MainActivity.this);
      Toast.makeText(MainActivity.this, "Pre execute is called", Toast.LENGTH_SHORT).show();
      Log.e("TAG", "onPreExecute: pre execut eis called very well" );
      progressDialog = ProgressDialog.show(MainActivity.this,"Image is Uploading","Please Wait",false,false);
    }

    @Override
    protected void onPostExecute(String string1) {

      super.onPostExecute(string1);

      // Dismiss the progress dialog after done uploading.
      progressDialog.dismiss();

      // Printing uploading success message coming from server on android app.
      Toast.makeText(MainActivity.this,string1,Toast.LENGTH_LONG).show();

      // Setting image as transparent after done uploading.
//        imageView.setImageResource(android.R.color.transparent);


    }

    @Override
    protected String doInBackground(Void... params) {

      ImageProcessClass imageProcessClass = new ImageProcessClass();

      HashMap<String,String> HashMapParams = new HashMap<String,String>();

      HashMapParams.put(ImageName, GetImageNameEditText);

      HashMapParams.put(ImagePath, ConvertImage);

      String FinalData = imageProcessClass.ImageHttpRequest(ServerUploadPath, HashMapParams);

      return FinalData;
    }
  }
  public class ImageProcessClass{

    public String ImageHttpRequest(String requestURL,HashMap<String, String> PData) {

      StringBuilder stringBuilder = new StringBuilder();
      Log.e("HTTP request","HTTPS request is created "+requestURL);

      try {

        URL url;
        HttpURLConnection httpURLConnectionObject ;
        OutputStream OutPutStream;
        BufferedWriter bufferedWriterObject ;
        BufferedReader bufferedReaderObject ;
        int RC ;

        url = new URL(requestURL);

        httpURLConnectionObject = (HttpURLConnection) url.openConnection();

        httpURLConnectionObject.setReadTimeout(19000);

        httpURLConnectionObject.setConnectTimeout(19000);



        httpURLConnectionObject.setRequestMethod("POST");

        httpURLConnectionObject.setDoInput(true);

        httpURLConnectionObject.setDoOutput(true);

        OutPutStream = httpURLConnectionObject.getOutputStream();

        bufferedWriterObject = new BufferedWriter(

                new OutputStreamWriter(OutPutStream, "UTF-8"));

        bufferedWriterObject.write(bufferedWriterDataFN(PData));

        bufferedWriterObject.flush();

        bufferedWriterObject.close();

        OutPutStream.close();

        RC = httpURLConnectionObject.getResponseCode();

        if (RC == HttpsURLConnection.HTTP_OK) {

          bufferedReaderObject = new BufferedReader(new InputStreamReader(httpURLConnectionObject.getInputStream()));
          Log.e("TAG", "ImageHttpRequest: Ok response" );
          stringBuilder = new StringBuilder();

          String RC2;

          while ((RC2 = bufferedReaderObject.readLine()) != null){

            stringBuilder.append(RC2);
          }
        }

      } catch (Exception e) {
        e.printStackTrace();
        Log.e("tag is error and error ", "ImageHttpRequest: Error is "+e );
      }
      Log.e("HTTP request","HTTPS request is created and result is "+stringBuilder.toString());
      return stringBuilder.toString();
    }

    private String bufferedWriterDataFN(HashMap<String, String> HashMapParams) throws UnsupportedEncodingException {

      StringBuilder stringBuilderObject;

      stringBuilderObject = new StringBuilder();

      for (Map.Entry<String, String> KEY : HashMapParams.entrySet()) {

        if (check)

          check = false;
        else
          stringBuilderObject.append("&");

        stringBuilderObject.append(URLEncoder.encode(KEY.getKey(), "UTF-8"));

        stringBuilderObject.append("=");

        stringBuilderObject.append(URLEncoder.encode(KEY.getValue(), "UTF-8"));
      }

      Log.e("Image sent", "bufferedWriterDataFN: image sendiong url is "+stringBuilderObject.toString() );
      return stringBuilderObject.toString();
    }

  }

}