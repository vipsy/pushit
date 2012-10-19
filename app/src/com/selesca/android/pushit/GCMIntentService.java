package com.selesca.android.pushit;

import com.google.android.gcm.GCMBaseIntentService;
import com.idmission.apps.core.Idm;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.text.ClipboardManager;
import android.util.Log;
import android.widget.Toast;

import com.selesca.android.pushit.utils.AppSettings;
import com.selesca.android.pushit.ws.WSRegister;

public class GCMIntentService extends GCMBaseIntentService {
	private static final String TAG = "PUSHIT:"
			+ GCMBaseIntentService.class.getSimpleName() + ": ";

	public GCMIntentService() {
		super(AppSettings.SENDER_ID);
	}

	@Override
	protected void onMessage(Context context, Intent intent) {
		// Idm.setContext(context);
		String data = intent.getExtras().getString("data");
		String action_id = intent.getExtras().getString("action_id");

		Log.i(TAG, "GCM Message action_id: " + action_id);
		Log.i(TAG, "GCM Message data: " + data);

		handleMessage(action_id, data);

		// Toast.makeText(getApplicationContext(),
		// intent.getExtas().getString("data"), Toast.LENGTH_SHORT).show();
	}

	private void handleMessage(String action_id, String data) {
		try {
			if (action_id.equals("sms")) {
				Intent smsIntent = new Intent(Intent.ACTION_VIEW);
				smsIntent.setData(Uri.parse("sms:"));
				smsIntent.putExtra("sms_body", data);
				smsIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
				startActivity(smsIntent);
			} else if (action_id.equals("email")) {
				Intent emailIntent = new Intent(
						android.content.Intent.ACTION_SEND);
				emailIntent.setType("plain/text");
				emailIntent.putExtra(android.content.Intent.EXTRA_TEXT, data);
				emailIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
				startActivity(emailIntent);
			} else if (action_id.equals("call")) {

				Uri callUri = Uri.parse("tel:" + data.trim());
				Intent callIntent = new Intent(
						android.content.Intent.ACTION_CALL, callUri);
				callIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
				startActivity(callIntent);

				/* Launch gtalk code */
				/*
				 * String[] dataList = data.split(","); Uri imUri = new
				 * Uri.Builder
				 * ().scheme("imto").authority("gtalk").appendPath(dataList
				 * [0]).build(); Intent intent = new
				 * Intent(Intent.ACTION_SENDTO, imUri);
				 * intent.putExtra(Intent.EXTRA_TEXT, dataList[1]);
				 * intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
				 * startActivity(intent);
				 */

			} else if (action_id.equals("browse")) {
				String url = data.trim();
				Intent intent = new Intent(Intent.ACTION_VIEW);
				intent.setData(Uri.parse(url));
				intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
				startActivity(intent);
			} else if (action_id.equals("copy")) {
				@SuppressWarnings("deprecation")
				ClipboardManager clipboard = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
				clipboard.setText(data.trim());
				Toast.makeText(this, "Text copied to clipboard",
						Toast.LENGTH_SHORT).show();
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	@Override
	protected void onRegistered(Context context, String regId) {
		Idm.setContext(context);
		Log.i("PUSHIT", "onRegistered:  regId= " + regId);
		AppSettings.setGCMRegId(regId);
		new WSRegister(AppSettings.getUsername(), AppSettings.getPassword(),
				AppSettings.getGCMRegId()).execute();
	}

	@Override
	protected void onUnregistered(Context context, String regId) {
		Idm.setContext(context);
		AppSettings.setGCMRegId("");
		new WSRegister(AppSettings.getUsername(), AppSettings.getPassword(), "")
				.execute();
	}

	@Override
	protected void onError(Context context, String errorId) {
		Idm.setContext(context);
		// TODO Auto-generated method stub

	}

	@Override
	protected boolean onRecoverableError(Context context, String errorId) {
		// TODO Auto-generated method stub
		Idm.setContext(context);
		return super.onRecoverableError(context, errorId);
	}

}
