package com.selesca.android.pushit.utils;


public class AppSettings extends com.idmission.apps.core.AppSettings {
	
	public static String SENDER_ID = "254929753609"; 
	
	private static String  GCM_REG_ID = "GCM_REG_ID";
	
	public static void setGCMRegId(String regId){
		AppSettings.setString(GCM_REG_ID, regId);
	}
	
	public static String getGCMRegId() {
		return AppSettings.getString(GCM_REG_ID, "");
	}

}
