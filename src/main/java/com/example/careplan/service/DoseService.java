package com.example.careplan.service;

import com.example.careplan.dto.DoseLogRequest;
import com.example.careplan.dto.DoseLogResponse;
import com.example.careplan.dto.DoseResponse;
import com.example.careplan.dto.MissedDoseResponse;
import com.example.careplan.entity.DoseLog;
import com.example.careplan.entity.Medicine;
import com.example.careplan.entity.Schedule;
import com.example.careplan.enums.DoseStatus;
import com.example.careplan.exception.BusinessRuleException;
import com.example.careplan.exception.ResourceNotFoundException;
import com.example.careplan.repository.DoseLogRepository;
import com.example.careplan.repository.MedicineRepository;
import com.example.careplan.repository.ScheduleRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class DoseService {

    private final MedicineRepository medicineRepository;
    private final ScheduleRepository scheduleRepository;
    private final DoseLogRepository doseLogRepository;
    private final EmailService emailService;

    public DoseService(MedicineRepository medicineRepository, ScheduleRepository scheduleRepository, DoseLogRepository doseLogRepository, EmailService emailService) {
        this.medicineRepository = medicineRepository;
        this.scheduleRepository = scheduleRepository;
        this.doseLogRepository = doseLogRepository;
        this.emailService = emailService;
    }

    public List<DoseResponse> getExpectedDosesForToday(Long patientId) {
        List<Medicine> medicines = medicineRepository.findByPatientId(patientId);
        List<DoseResponse> todayDoses = new ArrayList<>();
        LocalDate today = LocalDate.now();
        LocalTime now = LocalTime.now();

        for (Medicine medicine : medicines) {
            List<Schedule> schedules = scheduleRepository.findByMedicineId(medicine.getId());
            for (Schedule schedule : schedules) {
                Optional<DoseLog> logOpt = doseLogRepository.findByScheduleIdAndScheduledDate(schedule.getId(), today);
                DoseStatus currentStatus = DoseStatus.EXPECTED;

                if (logOpt.isPresent()) {
                    currentStatus = logOpt.get().getStatus();
                } else {
                    if (now.isAfter(schedule.getExpectedTime().plusHours(1))) {
                        currentStatus = DoseStatus.OVERDUE;
                        
                        // Save it so we don't spam emails on every fetch
                        DoseLog overdueLog = new DoseLog();
                        overdueLog.setSchedule(schedule);
                        overdueLog.setScheduledDate(today);
                        overdueLog.setStatus(DoseStatus.OVERDUE);
                        overdueLog.setLoggedAt(LocalDateTime.now());
                        doseLogRepository.save(overdueLog);

                        emailService.sendOverdueAlert(medicine.getPatient().getEmail(), medicine.getName());
                    }
                }

                DoseResponse response = new DoseResponse(
                        patientId,
                        medicine.getPatient().getName(),
                        medicine.getId(),
                        medicine.getName(),
                        medicine.getDosage(),
                        schedule.getId(),
                        schedule.getExpectedTime(),
                        currentStatus
                );
                todayDoses.add(response);
            }
        }
        return todayDoses;
    }

    @Transactional
    public DoseLogResponse logDose(DoseLogRequest request) {
        Schedule schedule = scheduleRepository.findById(request.getScheduleId())
                .orElseThrow(() -> new ResourceNotFoundException("Schedule not found with ID: " + request.getScheduleId()));

        if (request.getStatus() != DoseStatus.TAKEN && request.getStatus() != DoseStatus.MISSED) {
            throw new BusinessRuleException("Status must be TAKEN or MISSED");
        }

        Optional<DoseLog> existingLogOpt = doseLogRepository.findByScheduleIdAndScheduledDate(schedule.getId(), request.getScheduledDate());
        
        if (existingLogOpt.isPresent()) {
            DoseLog existingLog = existingLogOpt.get();
            if (existingLog.getStatus() == DoseStatus.TAKEN && request.getStatus() == DoseStatus.TAKEN) {
                throw new BusinessRuleException("Dose has already been marked as taken for this scheduled time.");
            }
            existingLog.setStatus(request.getStatus());
            existingLog.setLoggedAt(LocalDateTime.now());
            DoseLog saved = doseLogRepository.save(existingLog);
            return new DoseLogResponse(saved.getId(), saved.getSchedule().getId(), saved.getScheduledDate(), saved.getStatus().name(), saved.getLoggedAt());
        }

        DoseLog newLog = new DoseLog();
        newLog.setSchedule(schedule);
        newLog.setScheduledDate(request.getScheduledDate());
        newLog.setStatus(request.getStatus());
        newLog.setLoggedAt(LocalDateTime.now());
        
        DoseLog saved = doseLogRepository.save(newLog);
        return new DoseLogResponse(saved.getId(), saved.getSchedule().getId(), saved.getScheduledDate(), saved.getStatus().name(), saved.getLoggedAt());
    }

    public List<MissedDoseResponse> getMissedDoses(Long patientId, LocalDate startDate, LocalDate endDate) {
        if (startDate.isAfter(endDate)) {
            throw new BusinessRuleException("Start date cannot be after end date.");
        }
        List<DoseLog> missedLogs = doseLogRepository.findMissedDosesForPatient(patientId, DoseStatus.MISSED, startDate, endDate);
        List<MissedDoseResponse> responses = new ArrayList<>();
        for (DoseLog log : missedLogs) {
            responses.add(new MissedDoseResponse(
                    log.getId(),
                    log.getSchedule().getMedicine().getName(),
                    log.getSchedule().getMedicine().getDosage(),
                    log.getScheduledDate(),
                    log.getSchedule().getExpectedTime(),
                    log.getLoggedAt(),
                    log.getStatus()
            ));
        }
        return responses;
    }
}
