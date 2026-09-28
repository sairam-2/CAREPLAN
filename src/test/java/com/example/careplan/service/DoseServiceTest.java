package com.example.careplan.service;

import com.example.careplan.dto.DoseLogRequest;
import com.example.careplan.entity.DoseLog;
import com.example.careplan.entity.Schedule;
import com.example.careplan.enums.DoseStatus;
import com.example.careplan.exception.BusinessRuleException;
import com.example.careplan.repository.DoseLogRepository;
import com.example.careplan.repository.MedicineRepository;
import com.example.careplan.repository.ScheduleRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.time.LocalDate;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class DoseServiceTest {

    @Mock
    private ScheduleRepository scheduleRepository;

    @Mock
    private DoseLogRepository doseLogRepository;

    @Mock
    private MedicineRepository medicineRepository;

    @InjectMocks
    private DoseService doseService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testLogDose_DuplicateTaken_ThrowsException() {
        Long scheduleId = 1L;
        LocalDate date = LocalDate.now();

        DoseLogRequest request = new DoseLogRequest();
        request.setScheduleId(scheduleId);
        request.setScheduledDate(date);
        request.setStatus(DoseStatus.TAKEN);

        Schedule schedule = new Schedule();
        schedule.setId(scheduleId);

        DoseLog existingLog = new DoseLog();
        existingLog.setStatus(DoseStatus.TAKEN);

        when(scheduleRepository.findById(scheduleId)).thenReturn(Optional.of(schedule));
        when(doseLogRepository.findByScheduleIdAndScheduledDate(scheduleId, date))
                .thenReturn(Optional.of(existingLog));

        assertThrows(BusinessRuleException.class, () -> {
            doseService.logDose(request);
        });

        verify(doseLogRepository, never()).save(any());
    }
    
    @Test
    void testInvalidDateRange_ThrowsException() {
        assertThrows(BusinessRuleException.class, () -> {
            doseService.getMissedDoses(1L, LocalDate.now(), LocalDate.now().minusDays(1));
        });
    }
}
