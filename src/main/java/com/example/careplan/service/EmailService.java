package com.example.careplan.service;

import org.springframework.stereotype.Service;

@Service
public class EmailService {

    public void sendOverdueAlert(String toEmail, String medicineName) {
        if (toEmail == null || toEmail.trim().isEmpty()) {
            System.out.println("No email address provided. Skipping email alert for " + medicineName);
            return;
        }

        System.out.println("==================================================");
        System.out.println("✉️ SENDING OVERDUE ALERT EMAIL");
        System.out.println("To: " + toEmail);
        System.out.println("Subject: 🚨 URGENT: Overdue Medication Alert");
        System.out.println("Body:");
        System.out.println("Hello,");
        System.out.println("This is an automated alert from CAREPLAN.");
        System.out.println("Your scheduled dose for **" + medicineName + "** is now overdue by more than 1 hour.");
        System.out.println("Please take your medication as soon as possible and log it in the dashboard.");
        System.out.println("Stay healthy,\nCAREPLAN System");
        System.out.println("==================================================");
    }
}
