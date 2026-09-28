package com.example.careplan.repository;

import com.example.careplan.entity.DoseLog;
import com.example.careplan.enums.DoseStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface DoseLogRepository extends JpaRepository<DoseLog, Long> {
    Optional<DoseLog> findByScheduleIdAndScheduledDate(Long scheduleId, LocalDate scheduledDate);
    
    @Query("SELECT d FROM DoseLog d WHERE d.schedule.medicine.patient.id = :patientId AND d.status = :status AND d.scheduledDate BETWEEN :startDate AND :endDate")
    List<DoseLog> findMissedDosesForPatient(
            @Param("patientId") Long patientId, 
            @Param("status") DoseStatus status, 
            @Param("startDate") LocalDate startDate, 
            @Param("endDate") LocalDate endDate);
}
