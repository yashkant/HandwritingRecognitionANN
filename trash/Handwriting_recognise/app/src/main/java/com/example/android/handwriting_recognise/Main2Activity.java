package com.example.android.handwriting_recognise;

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;

public class zMain2Activity extends AppCompatActivity {
    private static final int SELECT_PICTURE = 1;
    ImageView imgBG;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        imgBG = (ImageView) findViewById(R.id.imgBG);
    }
    public void btnChooseBGClick(View v) {
        Intent i = new Intent(Intent.ACTION_PICK,
                android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(i, SELECT_PICTURE);
    }

    protected void onActivityResult(int requestCode, int resultCode,
                                    Intent imageReturnedIntent) {
        super.onActivityResult(requestCode, resultCode, imageReturnedIntent);

        switch (requestCode) {
            case SELECT_PICTURE:
                if (resultCode == RESULT_OK) {
                    Uri uri = imageReturnedIntent.getData();
                    String[] projection = { MediaStore.Images.Media.DATA };

                    Cursor cursor = getContentResolver().query(uri, projection,
                            null, null, null);
                    cursor.moveToFirst();

                    int columnIndex = cursor.getColumnIndex(projection[0]);
                    String filePath = cursor.getString(columnIndex);
                    cursor.close();

                    Bitmap yourSelectedImage = BitmapFactory.decodeFile(filePath);
                    Drawable d = new BitmapDrawable(yourSelectedImage);
                    imgBG.setBackgroundDrawable(d);
                }
        }
    }
}
