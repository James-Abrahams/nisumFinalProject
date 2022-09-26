package com.springkafka;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class KafkaListeners {

    @KafkaListener(
            topics = {"topic1", "topic2"},
            groupId = "groupId")
    void listener(String data) {

        System.out.println("Listener received: " + data);

    }

//    @KafkaListener(
//            topics = {"topic1"},
//            groupId = "groupId")
//    void listener1(String data) {
//        System.out.println("Listener received: " + data);
//    }
}
