package com.example.careplan.dto;

import java.time.LocalDate;
import java.time.LocalDateTime;

public class DoseLogResponse {
    private Long doseLogId;
    private Long scheduleId;
    private LocalDate scheduledDate;
    private String status;
    private LocalDateTime loggedAt;

    public DoseLogResponse(Long doseLogId, Long scheduleId, LocalDate scheduledDate, String status, LocalDateTime loggedAt) {
        this.doseLogId = doseLogId;
        this.scheduleId = scheduleId;
        this.scheduledDate = scheduledDate;
        this.status = status;
        this.loggedAt = loggedAt;
    }

    public Long getDoseLogId() { return doseLogId; }
    public Long getScheduleId() { return scheduleId; }
    public LocalDate getScheduledDate() { return scheduledDate; }
    public String getStatus() { return status; }
    public LocalDateTime getLoggedAt() { return loggedAt; }
}
