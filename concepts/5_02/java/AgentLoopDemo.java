public class AgentLoopDemo {
    enum State { START, TOOL, DONE }
    public static State next(State state, boolean hasToolCall) {
        if (state == State.DONE) return State.DONE;
        return hasToolCall ? State.TOOL : State.DONE;
    }
    public static void main(String[] args) {
        System.out.println(next(State.START, true));
    }
}
