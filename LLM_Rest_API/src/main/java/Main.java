import Server.RestApiServer;

import java.io.IOException;

public class Main {
    public static void main(String[] args) {

       // LlmClient.LanguageModelClient client = new LlmClient.LanguageModelClient();


        try {
            RestApiServer server = new RestApiServer();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }


/*
        //list models
        try {
         for(String e : client.listModels()){
             System.out.println(e);
         }
        } catch (IOException e) {
           e.printStackTrace();
        }
*/
/*
        //list running models
        try {
            for(LlmClient.LanguageModelClient.Model m : client.listRunningModels()){
                System.out.println(m.getModelName());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
*/
        /*
        //load model
        try {
           client.loadModel(LlmClient.LanguageModelClient.Model.LLAMA3_2_3B);
        } catch (IOException e) {
            e.printStackTrace();
        }
*/
/*
        //chat
        try {
         String s =   client.generateResponse("warum ist der himmerl blau", false);
            System.out.println(s);
        } catch (IOException e) {
            e.printStackTrace();
        }
*/
    }
}
