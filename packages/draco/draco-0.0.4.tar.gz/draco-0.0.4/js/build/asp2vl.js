"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const REGEX = /(\w+)\(([\w\.\/]+)(,([\w\.]+))?\)/;
/**
 * Convert from ASP to Vega-Lite.
 */
function asp2vl(facts) {
    let mark = '';
    let url = 'data/cars.json'; // default dataset
    const encodings = {};
    for (const value of facts) {
        // TODO: Better handle quoted fields. We currently simply remove all ".
        const cleanedValue = value.replace(/\"/g, '');
        const negSymbol = value.trim().startsWith(':-'); // TODO: remove this
        const [_, predicate, first, __, second] = REGEX.exec(cleanedValue);
        if (predicate === 'mark') {
            mark = first;
        }
        else if (predicate === 'data') {
            url = first;
        }
        else if (predicate !== 'violation') {
            if (!encodings[first]) {
                encodings[first] = {};
            }
            // if it contains the neg symbol, and the field is a boolean field, its value would be false
            // e.g., for the case ":- zero(e3)"
            encodings[first][predicate] = second || !negSymbol;
        }
    }
    const encoding = {};
    for (const e of Object.keys(encodings)) {
        const enc = encodings[e];
        // if quantitative encoding and zero is not set, set zero to false
        if (enc.type === 'quantitative' && enc.zero === undefined && enc.bin === undefined) {
            enc.zero = false;
        }
        const scale = Object.assign({}, (enc.log ? { type: 'log' } : {}), (enc.zero === undefined ? {} : enc.zero ? { zero: true } : { zero: false }));
        encoding[enc.channel] = Object.assign({ type: enc.type }, (enc.aggregate ? { aggregate: enc.aggregate } : {}), (enc.field ? { field: enc.field } : {}), (enc.stack ? { stack: enc.stack } : {}), (enc.bin !== undefined ? (+enc.bin === 10 ? { bin: true } : { bin: { maxbins: +enc.bin } }) : {}), (Object.keys(scale).length ? { scale } : {}));
    }
    return {
        $schema: 'https://vega.github.io/schema/vega-lite/v3.json',
        data: { url: `${url}` },
        mark,
        encoding,
    };
}
exports.default = asp2vl;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiYXNwMnZsLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4vc3JjL2FzcDJ2bC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOztBQUVBLE1BQU0sS0FBSyxHQUFHLG1DQUFtQyxDQUFDO0FBRWxEOztHQUVHO0FBQ0gsU0FBd0IsTUFBTSxDQUFDLEtBQWU7SUFDNUMsSUFBSSxJQUFJLEdBQUcsRUFBRSxDQUFDO0lBQ2QsSUFBSSxHQUFHLEdBQUcsZ0JBQWdCLENBQUMsQ0FBQyxrQkFBa0I7SUFDOUMsTUFBTSxTQUFTLEdBQTJCLEVBQUUsQ0FBQztJQUU3QyxLQUFLLE1BQU0sS0FBSyxJQUFJLEtBQUssRUFBRTtRQUN6Qix1RUFBdUU7UUFDdkUsTUFBTSxZQUFZLEdBQUcsS0FBSyxDQUFDLE9BQU8sQ0FBQyxLQUFLLEVBQUUsRUFBRSxDQUFDLENBQUM7UUFDOUMsTUFBTSxTQUFTLEdBQUcsS0FBSyxDQUFDLElBQUksRUFBRSxDQUFDLFVBQVUsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLG9CQUFvQjtRQUNyRSxNQUFNLENBQUMsQ0FBQyxFQUFFLFNBQVMsRUFBRSxLQUFLLEVBQUUsRUFBRSxFQUFFLE1BQU0sQ0FBQyxHQUFHLEtBQUssQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFRLENBQUM7UUFFMUUsSUFBSSxTQUFTLEtBQUssTUFBTSxFQUFFO1lBQ3hCLElBQUksR0FBRyxLQUFLLENBQUM7U0FDZDthQUFNLElBQUksU0FBUyxLQUFLLE1BQU0sRUFBRTtZQUMvQixHQUFHLEdBQUcsS0FBSyxDQUFDO1NBQ2I7YUFBTSxJQUFJLFNBQVMsS0FBSyxXQUFXLEVBQUU7WUFDcEMsSUFBSSxDQUFDLFNBQVMsQ0FBQyxLQUFLLENBQUMsRUFBRTtnQkFDckIsU0FBUyxDQUFDLEtBQUssQ0FBQyxHQUFHLEVBQUUsQ0FBQzthQUN2QjtZQUNELDRGQUE0RjtZQUM1RixtQ0FBbUM7WUFDbkMsU0FBUyxDQUFDLEtBQUssQ0FBQyxDQUFDLFNBQVMsQ0FBQyxHQUFHLE1BQU0sSUFBSSxDQUFDLFNBQVMsQ0FBQztTQUNwRDtLQUNGO0lBRUQsTUFBTSxRQUFRLEdBQStCLEVBQUUsQ0FBQztJQUVoRCxLQUFLLE1BQU0sQ0FBQyxJQUFJLE1BQU0sQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLEVBQUU7UUFDdEMsTUFBTSxHQUFHLEdBQUcsU0FBUyxDQUFDLENBQUMsQ0FBQyxDQUFDO1FBRXpCLGtFQUFrRTtRQUNsRSxJQUFJLEdBQUcsQ0FBQyxJQUFJLEtBQUssY0FBYyxJQUFJLEdBQUcsQ0FBQyxJQUFJLEtBQUssU0FBUyxJQUFJLEdBQUcsQ0FBQyxHQUFHLEtBQUssU0FBUyxFQUFFO1lBQ2xGLEdBQUcsQ0FBQyxJQUFJLEdBQUcsS0FBSyxDQUFDO1NBQ2xCO1FBRUQsTUFBTSxLQUFLLHFCQUNOLENBQUMsR0FBRyxDQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsRUFBRSxJQUFJLEVBQUUsS0FBSyxFQUFFLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUNoQyxDQUFDLEdBQUcsQ0FBQyxJQUFJLEtBQUssU0FBUyxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsQ0FBQyxDQUFDLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxDQUFDLENBQUMsQ0FBQyxFQUFFLElBQUksRUFBRSxLQUFLLEVBQUUsQ0FBQyxDQUMvRSxDQUFDO1FBRUYsUUFBUSxDQUFDLEdBQUcsQ0FBQyxPQUFPLENBQUMsbUJBQ25CLElBQUksRUFBRSxHQUFHLENBQUMsSUFBSSxJQUNYLENBQUMsR0FBRyxDQUFDLFNBQVMsQ0FBQyxDQUFDLENBQUMsRUFBRSxTQUFTLEVBQUUsR0FBRyxDQUFDLFNBQVMsRUFBRSxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsRUFDbkQsQ0FBQyxHQUFHLENBQUMsS0FBSyxDQUFDLENBQUMsQ0FBQyxFQUFFLEtBQUssRUFBRSxHQUFHLENBQUMsS0FBSyxFQUFFLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUN2QyxDQUFDLEdBQUcsQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLEVBQUUsS0FBSyxFQUFFLEdBQUcsQ0FBQyxLQUFLLEVBQUUsQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDLEVBQ3ZDLENBQUMsR0FBRyxDQUFDLEdBQUcsS0FBSyxTQUFTLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxHQUFHLENBQUMsR0FBRyxLQUFLLEVBQUUsQ0FBQyxDQUFDLENBQUMsRUFBRSxHQUFHLEVBQUUsSUFBSSxFQUFFLENBQUMsQ0FBQyxDQUFDLEVBQUUsR0FBRyxFQUFFLEVBQUUsT0FBTyxFQUFFLENBQUMsR0FBRyxDQUFDLEdBQUcsRUFBRSxFQUFFLENBQUMsQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDLEVBQ2pHLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQyxNQUFNLENBQUMsQ0FBQyxDQUFDLEVBQUUsS0FBSyxFQUFFLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxDQUNoRCxDQUFDO0tBQ0g7SUFFRCxPQUFPO1FBQ0wsT0FBTyxFQUFFLGlEQUFpRDtRQUMxRCxJQUFJLEVBQUUsRUFBRSxHQUFHLEVBQUUsR0FBRyxHQUFHLEVBQUUsRUFBRTtRQUN2QixJQUFJO1FBQ0osUUFBUTtLQUNrQixDQUFDO0FBQy9CLENBQUM7QUF4REQseUJBd0RDIn0=