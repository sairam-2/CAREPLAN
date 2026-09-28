import os

files = {
    'pom.xml': '''<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<project xmlns=\"http://maven.apache.org/POM/4.0.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd\">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.4</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.example</groupId>
    <artifactId>careplan</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>careplan</name>
    <description>Elderly Medicine Reminder Tracker</description>
    <properties>
        <java.version>17</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>''',

    'src/main/resources/application.properties': '''spring.application.name=careplan
spring.datasource.url=${DB_URL:jdbc:mysql://localhost:3306/careplan_db?createDatabaseIfNotExist=true}
spring.datasource.username=${DB_USERNAME:root}
spring.datasource.password=${DB_PASSWORD:root}
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

server.port=8080
''',

    'src/main/java/com/example/careplan/CarePlanApplication.java': '''package com.example.careplan;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CarePlanApplication {
    public static void main(String[] args) {
        SpringApplication.run(CarePlanApplication.class, args);
    }
}
''',

    'src/main/java/com/example/careplan/entity/Patient.java': '''package com.example.careplan.entity;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = \"patients\")
public class Patient {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @OneToMany(mappedBy = \"patient\", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Medicine> medicines;

    public Patient() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public List<Medicine> getMedicines() { return medicines; }
    public void setMedicines(List<Medicine> medicines) { this.medicines = medicines; }
}
''',

    'src/main/java/com/example/careplan/entity/Medicine.java': '''package com.example.careplan.entity;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = \"medicines\")
public class Medicine {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String dosage;

    @Column(nullable = false)
    private String frequency;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = \"patient_id\", nullable = false)
    private Patient patient;

    @OneToMany(mappedBy = \"medicine\", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Schedule> schedules;

    public Medicine() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDosage() { return dosage; }
    public void setDosage(String dosage) { this.dosage = dosage; }
    public String getFrequency() { return frequency; }
    public void setFrequency(String frequency) { this.frequency = frequency; }
    public Patient getPatient() { return patient; }
    public void setPatient(Patient patient) { this.patient = patient; }
    public List<Schedule> getSchedules() { return schedules; }
    public void setSchedules(List<Schedule> schedules) { this.schedules = schedules; }
}
''',

    'src/main/java/com/example/careplan/entity/Schedule.java': '''package com.example.careplan.entity;

import jakarta.persistence.*;
import java.time.LocalTime;

@Entity
@Table(name = \"schedules\")
public class Schedule {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalTime expectedTime;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = \"medicine_id\", nullable = false)
    private Medicine medicine;

    public Schedule() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public LocalTime getExpectedTime() { return expectedTime; }
    public void setExpectedTime(LocalTime expectedTime) { this.expectedTime = expectedTime; }
    public Medicine getMedicine() { return medicine; }
    public void setMedicine(Medicine medicine) { this.medicine = medicine; }
}
''',

    'src/main/java/com/example/careplan/entity/DoseLog.java': '''package com.example.careplan.entity;

import com.example.careplan.enums.DoseStatus;
import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = \"dose_logs\")
public class DoseLog {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = \"schedule_id\", nullable = false)
    private Schedule schedule;

    @Column(nullable = false)
    private LocalDate scheduledDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private DoseStatus status;

    @Column(nullable = false)
    private LocalDateTime loggedAt;

    public DoseLog() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Schedule getSchedule() { return schedule; }
    public void setSchedule(Schedule schedule) { this.schedule = schedule; }
    public LocalDate getScheduledDate() { return scheduledDate; }
    public void setScheduledDate(LocalDate scheduledDate) { this.scheduledDate = scheduledDate; }
    public DoseStatus getStatus() { return status; }
    public void setStatus(DoseStatus status) { this.status = status; }
    public LocalDateTime getLoggedAt() { return loggedAt; }
    public void setLoggedAt(LocalDateTime loggedAt) { this.loggedAt = loggedAt; }
}
''',

    'src/main/java/com/example/careplan/enums/DoseStatus.java': '''package com.example.careplan.enums;

public enum DoseStatus {
    EXPECTED,
    TAKEN,
    MISSED,
    OVERDUE
}
''',

    'src/main/java/com/example/careplan/repository/PatientRepository.java': '''package com.example.careplan.repository;

import com.example.careplan.entity.Patient;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PatientRepository extends JpaRepository<Patient, Long> {
}
''',

    'src/main/java/com/example/careplan/repository/MedicineRepository.java': '''package com.example.careplan.repository;

import com.example.careplan.entity.Medicine;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface MedicineRepository extends JpaRepository<Medicine, Long> {
    List<Medicine> findByPatientId(Long patientId);
}
''',

    'src/main/java/com/example/careplan/repository/ScheduleRepository.java': '''package com.example.careplan.repository;

import com.example.careplan.entity.Schedule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface ScheduleRepository extends JpaRepository<Schedule, Long> {
    List<Schedule> findByMedicineId(Long medicineId);
}
''',

    'src/main/java/com/example/careplan/repository/DoseLogRepository.java': '''package com.example.careplan.repository;

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
    
    @Query(\"SELECT d FROM DoseLog d WHERE d.schedule.medicine.patient.id = :patientId AND d.status = :status AND d.scheduledDate BETWEEN :startDate AND :endDate\")
    List<DoseLog> findMissedDosesForPatient(
            @Param(\"patientId\") Long patientId, 
            @Param(\"status\") DoseStatus status, 
            @Param(\"startDate\") LocalDate startDate, 
            @Param(\"endDate\") LocalDate endDate);
}
''',

    'src/main/java/com/example/careplan/dto/PatientRequest.java': '''package com.example.careplan.dto;

import jakarta.validation.constraints.NotBlank;

public class PatientRequest {
    @NotBlank(message = \"Patient name is required\")
    private String name;

    public PatientRequest() {}

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}
''',

    'src/main/java/com/example/careplan/dto/AddMedicineRequest.java': '''package com.example.careplan.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import java.time.LocalTime;
import java.util.List;

public class AddMedicineRequest {
    @NotNull(message = \"Patient ID is required\")
    private Long patientId;

    @NotBlank(message = \"Medicine name is required\")
    private String name;

    @NotBlank(message = \"Dosage is required\")
    private String dosage;

    @NotBlank(message = \"Frequency is required\")
    private String frequency;

    @NotEmpty(message = \"At least one scheduled time is required\")
    private List<LocalTime> timings;

    public AddMedicineRequest() {}

    public Long getPatientId() { return patientId; }
    public void setPatientId(Long patientId) { this.patientId = patientId; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDosage() { return dosage; }
    public void setDosage(String dosage) { this.dosage = dosage; }
    public String getFrequency() { return frequency; }
    public void setFrequency(String frequency) { this.frequency = frequency; }
    public List<LocalTime> getTimings() { return timings; }
    public void setTimings(List<LocalTime> timings) { this.timings = timings; }
}
''',

    'src/main/java/com/example/careplan/dto/MedicineResponse.java': '''package com.example.careplan.dto;

import java.time.LocalTime;
import java.util.List;

public class MedicineResponse {
    private Long id;
    private Long patientId;
    private String name;
    private String dosage;
    private String frequency;
    private List<LocalTime> timings;

    public MedicineResponse(Long id, Long patientId, String name, String dosage, String frequency, List<LocalTime> timings) {
        this.id = id;
        this.patientId = patientId;
        this.name = name;
        this.dosage = dosage;
        this.frequency = frequency;
        this.timings = timings;
    }

    public Long getId() { return id; }
    public Long getPatientId() { return patientId; }
    public String getName() { return name; }
    public String getDosage() { return dosage; }
    public String getFrequency() { return frequency; }
    public List<LocalTime> getTimings() { return timings; }
}
''',

    'src/main/java/com/example/careplan/dto/DoseLogRequest.java': '''package com.example.careplan.dto;

import com.example.careplan.enums.DoseStatus;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDate;

public class DoseLogRequest {
    @NotNull(message = \"Schedule ID is required\")
    private Long scheduleId;

    @NotNull(message = \"Scheduled date is required\")
    private LocalDate scheduledDate;

    @NotNull(message = \"Status is required (TAKEN or MISSED)\")
    private DoseStatus status;

    public DoseLogRequest() {}

    public Long getScheduleId() { return scheduleId; }
    public void setScheduleId(Long scheduleId) { this.scheduleId = scheduleId; }
    public LocalDate getScheduledDate() { return scheduledDate; }
    public void setScheduledDate(LocalDate scheduledDate) { this.scheduledDate = scheduledDate; }
    public DoseStatus getStatus() { return status; }
    public void setStatus(DoseStatus status) { this.status = status; }
}
''',

    'src/main/java/com/example/careplan/dto/DoseResponse.java': '''package com.example.careplan.dto;

import com.example.careplan.enums.DoseStatus;
import java.time.LocalTime;

public class DoseResponse {
    private Long patientId;
    private Long medicineId;
    private String medicineName;
    private String dosage;
    private Long scheduleId;
    private LocalTime scheduledTime;
    private DoseStatus status;

    public DoseResponse(Long patientId, Long medicineId, String medicineName, String dosage, Long scheduleId, LocalTime scheduledTime, DoseStatus status) {
        this.patientId = patientId;
        this.medicineId = medicineId;
        this.medicineName = medicineName;
        this.dosage = dosage;
        this.scheduleId = scheduleId;
        this.scheduledTime = scheduledTime;
        this.status = status;
    }

    public Long getPatientId() { return patientId; }
    public Long getMedicineId() { return medicineId; }
    public String getMedicineName() { return medicineName; }
    public String getDosage() { return dosage; }
    public Long getScheduleId() { return scheduleId; }
    public LocalTime getScheduledTime() { return scheduledTime; }
    public DoseStatus getStatus() { return status; }
}
''',

    'src/main/java/com/example/careplan/dto/DoseLogResponse.java': '''package com.example.careplan.dto;

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
''',

    'src/main/java/com/example/careplan/dto/MissedDoseResponse.java': '''package com.example.careplan.dto;

import java.time.LocalDate;
import java.time.LocalTime;

public class MissedDoseResponse {
    private Long doseLogId;
    private String medicineName;
    private String dosage;
    private LocalDate scheduledDate;
    private LocalTime scheduledTime;

    public MissedDoseResponse(Long doseLogId, String medicineName, String dosage, LocalDate scheduledDate, LocalTime scheduledTime) {
        this.doseLogId = doseLogId;
        this.medicineName = medicineName;
        this.dosage = dosage;
        this.scheduledDate = scheduledDate;
        this.scheduledTime = scheduledTime;
    }

    public Long getDoseLogId() { return doseLogId; }
    public String getMedicineName() { return medicineName; }
    public String getDosage() { return dosage; }
    public LocalDate getScheduledDate() { return scheduledDate; }
    public LocalTime getScheduledTime() { return scheduledTime; }
}
''',

    'src/main/java/com/example/careplan/dto/ErrorResponse.java': '''package com.example.careplan.dto;

import java.time.LocalDateTime;

public class ErrorResponse {
    private LocalDateTime timestamp;
    private int status;
    private String message;

    public ErrorResponse(LocalDateTime timestamp, int status, String message) {
        this.timestamp = timestamp;
        this.status = status;
        this.message = message;
    }

    public LocalDateTime getTimestamp() { return timestamp; }
    public int getStatus() { return status; }
    public String getMessage() { return message; }
}
''',

    'src/main/java/com/example/careplan/exception/BusinessRuleException.java': '''package com.example.careplan.exception;

public class BusinessRuleException extends RuntimeException {
    public BusinessRuleException(String message) {
        super(message);
    }
}
''',

    'src/main/java/com/example/careplan/exception/ResourceNotFoundException.java': '''package com.example.careplan.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
''',

    'src/main/java/com/example/careplan/exception/GlobalExceptionHandler.java': '''package com.example.careplan.exception;

import com.example.careplan.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessRuleException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleBusinessRuleException(BusinessRuleException ex) {
        return new ErrorResponse(LocalDateTime.now(), HttpStatus.BAD_REQUEST.value(), ex.getMessage());
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleResourceNotFoundException(ResourceNotFoundException ex) {
        return new ErrorResponse(LocalDateTime.now(), HttpStatus.NOT_FOUND.value(), ex.getMessage());
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidationException(MethodArgumentNotValidException ex) {
        String msg = ex.getBindingResult().getAllErrors().get(0).getDefaultMessage();
        return new ErrorResponse(LocalDateTime.now(), HttpStatus.BAD_REQUEST.value(), msg);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleGlobalException(Exception ex) {
        return new ErrorResponse(LocalDateTime.now(), HttpStatus.INTERNAL_SERVER_ERROR.value(), \"An unexpected error occurred.\");
    }
}
''',

    'src/main/java/com/example/careplan/service/PatientService.java': '''package com.example.careplan.service;

import com.example.careplan.dto.PatientRequest;
import com.example.careplan.entity.Patient;
import com.example.careplan.repository.PatientRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PatientService {
    
    private final PatientRepository patientRepository;
    
    public PatientService(PatientRepository patientRepository) {
        this.patientRepository = patientRepository;
    }
    
    public Patient addPatient(PatientRequest request) {
        Patient patient = new Patient();
        patient.setName(request.getName());
        return patientRepository.save(patient);
    }
    
    public List<Patient> getAllPatients() {
        return patientRepository.findAll();
    }
}
''',

    'src/main/java/com/example/careplan/service/MedicineService.java': '''package com.example.careplan.service;

import com.example.careplan.dto.AddMedicineRequest;
import com.example.careplan.dto.MedicineResponse;
import com.example.careplan.entity.Medicine;
import com.example.careplan.entity.Patient;
import com.example.careplan.entity.Schedule;
import com.example.careplan.exception.ResourceNotFoundException;
import com.example.careplan.repository.MedicineRepository;
import com.example.careplan.repository.PatientRepository;
import com.example.careplan.repository.ScheduleRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class MedicineService {

    private final MedicineRepository medicineRepository;
    private final PatientRepository patientRepository;
    private final ScheduleRepository scheduleRepository;

    public MedicineService(MedicineRepository medicineRepository, PatientRepository patientRepository, ScheduleRepository scheduleRepository) {
        this.medicineRepository = medicineRepository;
        this.patientRepository = patientRepository;
        this.scheduleRepository = scheduleRepository;
    }

    @Transactional
    public MedicineResponse addMedicine(AddMedicineRequest request) {
        Patient patient = patientRepository.findById(request.getPatientId())
                .orElseThrow(() -> new ResourceNotFoundException(\"Patient not found with ID: \" + request.getPatientId()));

        Medicine medicine = new Medicine();
        medicine.setPatient(patient);
        medicine.setName(request.getName());
        medicine.setDosage(request.getDosage());
        medicine.setFrequency(request.getFrequency());

        Medicine savedMedicine = medicineRepository.save(medicine);
        List<LocalTime> savedTimings = new ArrayList<>();

        for (LocalTime time : request.getTimings()) {
            Schedule schedule = new Schedule();
            schedule.setExpectedTime(time);
            schedule.setMedicine(savedMedicine);
            scheduleRepository.save(schedule);
            savedTimings.add(time);
        }

        return new MedicineResponse(savedMedicine.getId(), patient.getId(), savedMedicine.getName(), savedMedicine.getDosage(), savedMedicine.getFrequency(), savedTimings);
    }
}
''',

    'src/main/java/com/example/careplan/service/DoseService.java': '''package com.example.careplan.service;

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

    public DoseService(MedicineRepository medicineRepository, ScheduleRepository scheduleRepository, DoseLogRepository doseLogRepository) {
        this.medicineRepository = medicineRepository;
        this.scheduleRepository = scheduleRepository;
        this.doseLogRepository = doseLogRepository;
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
                    }
                }

                DoseResponse response = new DoseResponse(
                        patientId,
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
                .orElseThrow(() -> new ResourceNotFoundException(\"Schedule not found with ID: \" + request.getScheduleId()));

        if (request.getStatus() != DoseStatus.TAKEN && request.getStatus() != DoseStatus.MISSED) {
            throw new BusinessRuleException(\"Status must be TAKEN or MISSED\");
        }

        Optional<DoseLog> existingLogOpt = doseLogRepository.findByScheduleIdAndScheduledDate(schedule.getId(), request.getScheduledDate());
        
        if (existingLogOpt.isPresent()) {
            DoseLog existingLog = existingLogOpt.get();
            if (existingLog.getStatus() == DoseStatus.TAKEN && request.getStatus() == DoseStatus.TAKEN) {
                throw new BusinessRuleException(\"Dose has already been marked as taken for this scheduled time.\");
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
            throw new BusinessRuleException(\"Start date cannot be after end date.\");
        }
        List<DoseLog> missedLogs = doseLogRepository.findMissedDosesForPatient(patientId, DoseStatus.MISSED, startDate, endDate);
        List<MissedDoseResponse> responses = new ArrayList<>();
        for (DoseLog log : missedLogs) {
            responses.add(new MissedDoseResponse(
                    log.getId(),
                    log.getSchedule().getMedicine().getName(),
                    log.getSchedule().getMedicine().getDosage(),
                    log.getScheduledDate(),
                    log.getSchedule().getExpectedTime()
            ));
        }
        return responses;
    }
}
''',

    'src/main/java/com/example/careplan/controller/PatientController.java': '''package com.example.careplan.controller;

import com.example.careplan.dto.PatientRequest;
import com.example.careplan.entity.Patient;
import com.example.careplan.service.PatientService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping(\"/api/patients\")
public class PatientController {

    private final PatientService patientService;

    public PatientController(PatientService patientService) {
        this.patientService = patientService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Patient addPatient(@Valid @RequestBody PatientRequest request) {
        return patientService.addPatient(request);
    }

    @GetMapping
    public List<Patient> getAllPatients() {
        return patientService.getAllPatients();
    }
}
''',

    'src/main/java/com/example/careplan/controller/MedicineController.java': '''package com.example.careplan.controller;

import com.example.careplan.dto.AddMedicineRequest;
import com.example.careplan.dto.MedicineResponse;
import com.example.careplan.service.MedicineService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(\"/api/medicines\")
public class MedicineController {

    private final MedicineService medicineService;

    public MedicineController(MedicineService medicineService) {
        this.medicineService = medicineService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public MedicineResponse addMedicine(@Valid @RequestBody AddMedicineRequest request) {
        return medicineService.addMedicine(request);
    }
}
''',

    'src/main/java/com/example/careplan/controller/DoseController.java': '''package com.example.careplan.controller;

import com.example.careplan.dto.DoseLogRequest;
import com.example.careplan.dto.DoseLogResponse;
import com.example.careplan.dto.DoseResponse;
import com.example.careplan.dto.MissedDoseResponse;
import com.example.careplan.service.DoseService;
import jakarta.validation.Valid;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping(\"/api/doses\")
public class DoseController {

    private final DoseService doseService;

    public DoseController(DoseService doseService) {
        this.doseService = doseService;
    }

    @GetMapping(\"/today/patient/{patientId}\")
    public List<DoseResponse> getExpectedDosesForToday(@PathVariable Long patientId) {
        return doseService.getExpectedDosesForToday(patientId);
    }

    @PostMapping(\"/log\")
    public DoseLogResponse logDose(@Valid @RequestBody DoseLogRequest request) {
        return doseService.logDose(request);
    }

    @GetMapping(\"/missed/patient/{patientId}\")
    public List<MissedDoseResponse> getMissedDoses(
            @PathVariable Long patientId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        return doseService.getMissedDoses(patientId, startDate, endDate);
    }
}
''',

    'src/test/java/com/example/careplan/service/DoseServiceTest.java': '''package com.example.careplan.service;

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
'''
}

base_dir = 'd:/careplan'

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Successfully created all project files.')
