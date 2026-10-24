// Exercise the actual installed scheduler on this plan, without invoking agents/cloud.
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { sprintTasks } from "../gh-dynamic-workflows/loop-workflow.mjs";
import { validateTaskCards } from "../gh-dynamic-workflows/work-cards.mjs";
import { scheduleTasks, criticalPathPriorities, createResourceScheduler } from "../gh-dynamic-workflows/scheduling.mjs";

const plan = JSON.parse(await readFile(new URL("../docs/requirements/delivery-sprint-plan.json", import.meta.url), "utf8"));
const tasks = sprintTasks({ SprintPlan: plan }, { firstSprint: true });
validateTaskCards(tasks.map(({ id, workCard }) => ({ id, workCard })), tasks, "sprint planning test");
const priorities = criticalPathPriorities(tasks);
assert.equal(priorities.get(tasks[0].id), 410);
const events = [], completed = new Set(), independent = plan.dispatch.parallelAfterSkeleton;
let releaseFanout, concurrent = 0, maxConcurrent = 0;
const fanout = new Promise((resolve) => { releaseFanout = resolve; });
const outcome = await scheduleTasks(tasks, async (task) => {
    for (const dep of task.dependsOn) assert.ok(completed.has(dep), "dependency not accepted");
    events.push(`start:${task.id}`);
    if (independent.includes(task.id)) {
        concurrent++;
        maxConcurrent = Math.max(maxConcurrent, concurrent);
        if (concurrent === independent.length) releaseFanout();
        // A timeout fails rather than hanging if future changes accidentally serialize construction.
        let timer;
        try {
            await Promise.race([fanout, new Promise((_, reject) => {
                timer = setTimeout(() => reject(new Error("independent fanout serialized")), 2000);
            })]);
        } finally { clearTimeout(timer); }
        concurrent--;
    }
    completed.add(task.id);
    events.push(`accepted:${task.id}`);
    return { status: "agreed", taskId: task.id, synthetic: true };
});
assert.equal(maxConcurrent, 3);
assert.ok(outcome.every((item) => item.status === "agreed"));
console.log("Synthetic exact-plan dispatch: all 6 callbacks ran; max concurrent construction=3.");
console.log(events.join("\n"));

const failed = await scheduleTasks(tasks, async (task) => ({
    status: task.walkingSkeleton ? "rework" : "agreed", taskId: task.id,
}));
assert.equal(failed[0].status, "rework");
assert.ok(failed.slice(1).every((item) => item.status === "not-run"));
console.log("Synthetic failed skeleton: all 5 dependents remained not-run.");

const localized = await scheduleTasks(tasks, async (task) => ({
    status: task.id === "coordinator-blob-contract" ? "rework" : "agreed", taskId: task.id,
}));
assert.equal(localized.find((item) => item.taskId === "remote-specialist-revision").status, "agreed");
assert.equal(localized.find((item) => item.taskId === "terminal-evidence-surface").status, "agreed");
assert.equal(localized.find((item) => item.taskId === "continuity-recovery-isolation").status, "not-run");
assert.equal(localized.find((item) => item.taskId === "integrated-terminal-acceptance").status, "not-run");
console.log("Synthetic localized failure: independent work continued; actual dependents held.");

// The same shared resources cover each simulated DevOps-then-E2E pair.
const lock = createResourceScheduler();
let verifying = 0, peak = 0;
await Promise.all(independent.map((id) => lock(plan.exclusiveResources, async () => {
    verifying++;
    peak = Math.max(peak, verifying);
    events.push(`DevOpsWorkLoop:${id}`);
    await new Promise((resolve) => setImmediate(resolve));
    events.push(`EndToEndTestLoop:${id}`);
    assert.equal(verifying, 1);
    verifying--;
})));
assert.equal(peak, 1);
console.log("Synthetic shared-resource verification: max concurrency=1; lock spans DevOps then E2E.");
console.log("Runtime schema/card/dependency checks passed; no real assignments or deployment performed.");
