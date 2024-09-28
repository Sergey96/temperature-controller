#include <OneWire.h>

#include <DHT.h>
#define DHTPIN_TERMPERATURE 2 // Тот самый номер пина, о котором упоминалось выше
#define DHTPIN_HUMIDITY 4 // Тот самый номер пина, о котором упоминалось выше

OneWire ds(DHTPIN_TERMPERATURE);
DHT dht(DHTPIN_HUMIDITY, DHT11);


byte addr[8];
void setup() {
    Serial.begin(9600);
    dht.begin();
    ds.search(addr);
    ds.reset();
}

void loop() {
    byte i;
    byte data[12];
    float celsius;

    // поиск датчика
    ds.reset_search();
    bool isFound = ds.search(addr);

    if ( !isFound) {
        ds.reset_search();
        delay(250);
        return;
    }
    ds.reset();
    ds.select(addr);
    ds.write(0x44, 1); // измерение температуры

    delay(1000); 
    ds.reset();
    ds.select(addr); 
    ds.write(0xBE); // начало чтения измеренной температуры
    //показания температуры из внутренней памяти датчика
    for ( i = 0; i < 9; i++) {
        data[i] = ds.read();
    }
    int16_t raw = (data[1] << 8) | data[0];
    // датчик может быть настроен на разную точность, выясняем её 
    byte cfg = (data[4] & 0x60);
    if (cfg == 0x00) raw = raw & ~7; // точность 9-разрядов, 93,75 мс
    else if (cfg == 0x20) raw = raw & ~3; // точность 10-разрядов, 187,5 мс
    else if (cfg == 0x40) raw = raw & ~1; // точность 11-разрядов, 375 мс
    // преобразование показаний в градусы Цельсия 
    celsius = (float)raw / 16.0;

    float h = dht.readHumidity(); //Измеряем влажность
    float t = dht.readTemperature(); //Измеряем температуру
    // if (isnan(h) || isnan(t)) {  // Проверка. Если не удается считать показания, выводится «Ошибка считывания», и программа завершает работу
    //     Serial.println("Ошибка считывания");
    // }
    String outVal = String(celsius) + " | " + String(h) + " | " + String(t);
    Serial.println(outVal);
}
