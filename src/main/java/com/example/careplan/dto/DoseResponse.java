package com.example.careplan.dto;

import com.example.careplan.enums.DoseStatus;
import java.time.LocalTime;

public class DoseResponse {
    private Long patientId;
    private String patientName;
    private Long medicineId;
    private String medicineName;
    private String dosage;
    private Long scheduleId;
    private LocalTime scheduledTime;
    private DoseStatus status;

    public DoseResponse(Long patientId, String patientName, Long medicineId, String medicineName, String dosage, Long scheduleId, LocalTime scheduledTime, DoseStatus status) {
        this.patientId = patientId;
        this.patientName = patientName;
        this.medicineId = medicineId;
        this.medicineName = medicineName;
        this.dosage = dosage;
        this.scheduleId = scheduleId;
        this.scheduledTime = scheduledTime;
        this.status = status;
    }

    public Long getPatientId() { return patientId; }
    public String getPatientName() { return patientName; }
    public Long getMedicineId() { return medicineId; }
    public String getMedicineName() { return medicineName; }
    public String getDosage() { return dosage; }
    public Long getScheduleId() { return scheduleId; }
    public LocalTime getScheduledTime() { return scheduledTime; }
    public DoseStatus getStatus() { return status; }
}
