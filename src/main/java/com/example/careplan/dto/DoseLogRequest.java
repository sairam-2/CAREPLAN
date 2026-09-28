package com.example.careplan.dto;

import com.example.careplan.enums.DoseStatus;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDate;

public class DoseLogRequest {
    @NotNull(message = "Schedule ID is required")
    private Long scheduleId;

    @NotNull(message = "Scheduled date is required")
    private LocalDate scheduledDate;

    @NotNull(message = "Status is required (TAKEN or MISSED)")
    private DoseStatus status;

    public DoseLogRequest() {}

    public Long getScheduleId() { return scheduleId; }
    public void setScheduleId(Long scheduleId) { this.scheduleId = scheduleId; }
    public LocalDate getScheduledDate() { return scheduledDate; }
    public void setScheduledDate(LocalDate scheduledDate) { this.scheduledDate = scheduledDate; }
    public DoseStatus getStatus() { return status; }
    public void setStatus(DoseStatus status) { this.status = status; }
}
