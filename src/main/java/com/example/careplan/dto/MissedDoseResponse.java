package com.example.careplan.dto;

import com.example.careplan.enums.DoseStatus;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

public class MissedDoseResponse {
    private Long id;
    private String medicineName;
    private String dosage;
    private LocalDate scheduledDate;
    private LocalTime scheduledTime;
    private LocalDateTime loggedAt;
    private DoseStatus status;

    public MissedDoseResponse(Long id, String medicineName, String dosage, LocalDate scheduledDate, LocalTime scheduledTime, LocalDateTime loggedAt, DoseStatus status) {
        this.id = id;
        this.medicineName = medicineName;
        this.dosage = dosage;
        this.scheduledDate = scheduledDate;
        this.scheduledTime = scheduledTime;
        this.loggedAt = loggedAt;
        this.status = status;
    }

    public Long getId() { return id; }
    public String getMedicineName() { return medicineName; }
    public String getDosage() { return dosage; }
    public LocalDate getScheduledDate() { return scheduledDate; }
    public LocalTime getScheduledTime() { return scheduledTime; }
    public LocalDateTime getLoggedAt() { return loggedAt; }
    public DoseStatus getStatus() { return status; }
}
