#include <Arduino.h>

// Định nghĩa các chân
#define HN 42      // Cảm biến HN
#define Pump 59    // Điều khiển bơm

// Biến trạng thái
bool pumpActive = false;    // Trạng thái bơm
unsigned long previousMillis = 0; // Lưu thời gian trước đó
const unsigned long interval1 = 1000; // 1 giây
const unsigned long interval2 = 2000; // 2 giây
bool waitingForPump = false; // Cờ chờ bật bơm
bool waitingForStop = false; // Cờ chờ tắt bơm

void setup() {
  Serial.begin(115200);

  // Cài đặt chân
  pinMode(HN, INPUT_PULLUP); // Cảm biến HN với điện trở kéo lên
  pinMode(Pump, OUTPUT);     // Điều khiển bơm

  // Đặt trạng thái ban đầu
  digitalWrite(Pump, HIGH);  // Tắt bơm ban đầu
}

void loop() {
  // Đọc trạng thái cảm biến HN
  bool hnState = digitalRead(HN);

  if (hnState == HIGH && !pumpActive) {
    // Khi cảm biến HN phát hiện LOW
    Serial.println("Tắt chế độ quét QR"); // Gửi tín hiệu tắt quét QR
    previousMillis = millis();            // Ghi lại thời gian hiện tại
    waitingForPump = true;                // Đặt cờ chờ bật bơm
    pumpActive = true;                    // Đánh dấu bơm đang hoạt động
  }

  if (waitingForPump && millis() - previousMillis >= interval1) {
    // Sau 1 giây, bật bơm và chuyển sang chế độ YOLOv5
    digitalWrite(Pump, LOW);              // Bật bơm
    Serial.println("Chuyển sang chế độ YOLOv5"); // Gửi tín hiệu
    previousMillis = millis();            // Cập nhật thời gian
    waitingForPump = false;               // Tắt cờ bật bơm
    waitingForStop = true;                // Đặt cờ chờ tắt bơm
  }

  if (waitingForStop && millis() - previousMillis >= interval2) {
    // Sau 2 giây, ngừng bơm và bật lại chế độ quét QR
    digitalWrite(Pump, HIGH);             // Tắt bơm
    Serial.println("Bật lại chế độ quét QR"); // Gửi tín hiệu
    waitingForStop = false;               // Tắt cờ tắt bơm
    pumpActive = false;                   // Đặt lại trạng thái bơm
  }
}
